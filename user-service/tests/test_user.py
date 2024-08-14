from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"username": "testuser", "email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_user():
    response = client.put("/users/1", json={"username": "updateduser"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"

def test_update_profile_picture():
    with open("test_image.png", "wb") as f:
        f.write(b"fake image data")
    with open("test_image.png", "rb") as image_file:
        response = client.put("/users/1/profile-picture", files={"file": image_file})
    assert response.status_code == 200
    assert response.json() == {"message": "Profile picture updated"}

def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"message": "User account deactivated"}