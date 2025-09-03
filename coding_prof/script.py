import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone

# Parse JSON file & validate

def load_alerts(file_path):
   with open(file_path, "r") as f:
       data = json.load(f)

   if "alerts" not in data or not isinstance(data["alerts"], list):
       raise ValueError("Invalid JSON structure")

   return data["alerts"]

# Filter alerts by given criteria

def filter_alerts(alerts, severity=None, service=None, minutes=None):
   now = datetime.now(timezone.utc)
   filtered = []

   for alert in alerts:
       try:
           ts = datetime.fromisoformat(alert["timestamp"].replace("Z", "+00:00"))
       except Exception:
           continue

       if severity and alert["severity"] != severity:
           continue
       if service and alert["service"] != service:
           continue
       if minutes and ts < now - timedelta(minutes=minutes):
           continue

       filtered.append(alert)

   return filtered


# Group related alerts

def group_alerts(alerts):
   grouped = defaultdict(list)
   for alert in alerts:
       key = (alert["service"], alert["component"])
       grouped[key].append(alert)
   return grouped


# Calculate priority score (weighted algorithm)

def calculate_priority(alerts):
   severity_weight = {"critical": 10, "warning": 5, "info": 1}

   # count affected components per service
   components_per_service = defaultdict(set)
   for a in alerts:
       components_per_service[a["service"]].add(a["component"])


   scores = {}
   for a in alerts:
       sev_score = severity_weight.get(a["severity"], 0)

       try:
           deviation = (a["value"] - a["threshold"]) / a["threshold"] * 100
       except ZeroDivisionError:
           deviation = 0

       affected_components = len(components_per_service[a["service"]])

       score = sev_score + deviation + affected_components
       scores[a["id"]] = round(score, 2)


   return scores

if __name__ == "__main__":
   alerts = load_alerts("sample_alerts.json")

   print("\n--- All Alerts ---")
   for a in alerts:
       print(json.dumps(a, indent=2))

   print("\n--- Filtered (critical, payment-processor, last 15 min) ---")
   filtered = filter_alerts(alerts, severity="critical", service="payment-processor", minutes=15)
   for a in filtered:
       print(json.dumps(a, indent=2))

   print("\n--- Grouped Alerts ---")
   grouped = group_alerts(alerts)
   for key, group in grouped.items():
       print(f"{key}: {len(group)} alerts")

   print("\n--- Priority Scores ---")
   scores = calculate_priority(alerts)
   for alert_id, score in scores.items():
       print(f"Alert {alert_id} -> Priority: {score}")
