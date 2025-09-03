**Implemented the AKS deployment using a free account and some credits in Azure. Will delete the whole setup after 
completing this assignment to avoid unnecessary costs.**

**Note: I have referred a few websites/LLM for some installations/templates etc**

Execution steps:
1. Fork the repository to my own github account. Renamed it.
2. Clone to my local- git clone https://github.com/divyatiwari19/fastapi-app.git
3. Updated and fixed the main.py, test_main.py according to the best security practices. Kept only the required entries
   in the requirement.txt file and removed all others that were not required. Commented as needed inside the file.
4. Tested the app in local.
5. Created a Dockerfile.Built it using the below commands,
   docker build -t fastapp:v1 .

Also, can do image scanning.

6. docker run -d --name my-fastapp-container -p 8000:8000 divya19/fastapp:v1

curl and tested the app again: ****screenshots for the output of the curl commands are attached in the word document.**

- curl http://localhost:8000/
- curl http://localhost:8000/health
- curl "http://localhost:8000/items/42"
- curl "http://localhost:8000/items/42?q=testing"

Prerequisites for AKS deployment:
# Azure account
# Install Azure CLI
# Install Terraform
# Install kubectl
# Install Helm

**Execution:**

# az login
# az account set --subscription <your-subscription-id>

# Create ACR
# Get ACR credentials
az acr login --name myacrfastapp

# Tag & Push image
Created the ACR already.
docker tag fastapp:v1 myacrfastapp.azurecr.io/myfastapp:v1
docker push myacrfastapp.azurecr.io/myfastapp:v1

# Terraform commands
terraform init
terraform plan
terraform apply

# After the deployment
- Check if the pod is up and running. I got ErrImagePull error as there was some typo in the image name in the helm 
  values file.
- Can run various kubectl commands regarding what you want to check. Example- kubectl get nodes, kubectl get nodes etc.
- Check service- kubectl get svc fastapp.

 # Test the endpoints--> Real output screenshots are attached in the word document.
- dabbutiwari@MacBookPro terraform % curl http://4.245.91.247/                    
{"Hello":"World"}% 
- dabbutiwari@MacBookPro terraform % curl http://4.245.91.247/health              
{"status":"ok"}% 
- dabbutiwari@MacBookPro terraform % curl "http://4.245.91.247/items/42"          
{"item_id":42,"q":null}%
- dabbutiwari@MacBookPro terraform % curl "http://4.245.91.247/items/42?q=testing"
{"item_id":42,"q":"testing"}%


Trade-offs and improvements in the current setup:

- There are limitations when doing in the local/personal setup.
- Single AKS cluster and not isolated per environment. Multi-cluster/namespace are better Prod ones.
- ACR Authentication- this one is okay. but for multiple clusters or ACRs, need extra identities or SPNs.
- Image is being pushed manually here, but CI/CD integration would automate builds, tagging, and push in the actual work.
- LB service exposed app externally. Works fine for testing here, but LB in cloud can be expensive in prod, internal
  services or ingress controllers are better.
- Proper image tagging and versioning can be implemented.
- Good RBAC policies missing in this one. can be improved.
- Working on the main branch. I usually create a separate branch while working in the office, make changes/update and
  create a PR (as a best practice).
- Single default namespace which is not suitable for multiple environments(UAT, QA, Staging or Prod).
- Implement CI/CD setup that Automate Docker image build → push to ACR → Helm upgrade via Terraform or Helmfile. 
  Add automated testing, linting, and security scanning.
- Having multiple environments- UAT, QA, Staging, Prod.
- Use separate namespaces for dev, staging, and prod or create multiple clusters.
- Use NGINX / Azure Application Gateway ingress instead of a public LoadBalancer. Provides TLS termination, 
  path routing and cost efficiency.
- Enable Horizontal Pod Autoscaler (HPA) for FastAPI deployment based on CPU/memory or custom metrics. Also, Enable 
  liveness/readiness probes.
- Implement Terraform state management in remote backend (Azure Blob Storage or S3+Dynamo DB).
- Using proper IAM roles, policies/Azure Entra ID (previously Azure AD). Can also do PIM requests for better security
  for the production environments.
- Use extra secrets managers while doing the actual works. Use azure keyvault integration for secret management
  and rotate secrets in a timely manner.
- Implement monitoring dashboards/setup using Prometheus,Grafana for metrics and Azure Monitor/Log Analytics/ELK for 
  logs.
- Can also deploy some antivirus using helm.(I did it earlier for cortex agent- palo Alto Antivirus for my K8 clusters).
- Setting up the alerts separate for the non-prods and production and sending it to Slacks channels, Teams group. Can 
  integrate it with the Pagerduty for example in case of incident management etc.

   


