from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_payment():
    response = client.post("/payments/", json={"amount": 100.0, "currency": "USD", "payment_method_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 100.0
    assert data["currency"] == "USD"
    assert data["status"] == "pending"

def test_read_payment():
    response = client.get("/payments/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_create_transaction():
    response = client.post("/transactions/", json={"payment_id": 1, "transaction_id": "txn_123", "gateway": "stripe", "amount": 100.0, "currency": "USD"})
    assert response.status_code == 200
    data = response.json()
    assert data["transaction_id"] == "txn_123"
    assert data["gateway"] == "stripe"

def test_read_transaction():
    response = client.get("/transactions/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1