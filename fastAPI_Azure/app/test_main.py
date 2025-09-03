from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_read_item():
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": None}

def test_read_item_with_query():
    response = client.get("/items/42?q=testing")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": "testing"}

def test_update_item():
    data = {
        "name": "Test Item",
        "price": 19.99,
        "is_offer": True
    }
    response = client.put("/items/42", json=data)
    assert response.status_code == 200
    assert response.json() == {"item_name": "Test Item", "item_id": 42}

def test_update_item_validation_error_missing_name():
    # Missing required field name
    data = {"price": 10.0}
    resp = client.put("/items/1", json=data)
    assert resp.status_code == 422

def test_health_check():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}