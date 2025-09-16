from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_item():
    response = client.post("/items", json={"name": "Test", "price": 1.0, "quantity": 1})
    assert response.status_code == 200
    assert "id" in response.json()