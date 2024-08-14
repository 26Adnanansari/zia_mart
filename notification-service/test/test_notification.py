from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_notify_user():
    response = client.post("/notify/", json={"user_id": 1, "message": "Hello!"})
    assert response.status_code == 200
    assert response.json() == {"status": "Notification sent"}