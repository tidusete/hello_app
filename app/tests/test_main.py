from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_save_birthday():
    request_data = {
        "dateOfBirth": "2000-01-01"
    }
    with TestClient(app) as client:

        response = client.put("/hello/pepe", json=request_data)
        assert response.status_code == 204

def test_greet_user_found():
    with TestClient(app) as client:
        response = client.get("/hello/pepe")
        assert response.status_code == 200
        assert "message" in response.json()

def test_greet_user_not_found():
    with TestClient(app) as client:
        response = client.get("/hello/marcos")
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

def test_invalid_dob():
    request_data = {
        "dateOfBirth": "2050-01-01"
    }
    with TestClient(app) as client:
        response = client.put("/hello/victor", json=request_data)
        assert response.status_code == 400
        assert response.json() == {"detail": "Date of birth must be in the past"}
