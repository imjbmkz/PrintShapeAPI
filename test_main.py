import pytest
from fastapi.testclient import TestClient
from main import app

# Create a TestClient instance
client = TestClient(app)

# Valid credentials
USERNAME = "user"
PASSWORD = "pass"

# Helper function for basic authentication
def auth_headers(username=USERNAME, password=PASSWORD):
    import base64
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

# ------------------- SUCCESS TEST CASES -------------------

def test_draw_rectangle():
    response = client.post("/shape/rectangle?times=4", headers=auth_headers())
    assert response.status_code == 200
    assert response.json() == {"shape": "rectangle", "times": 4, "area": 16.0}

def test_draw_triangle():
    response = client.post("/shape/triangle?times=3", headers=auth_headers())
    assert response.status_code == 200
    assert response.json() == {"shape": "triangle", "times": 3, "area": 4.5}

def test_draw_diamond():
    response = client.post("/shape/diamond?times=5", headers=auth_headers())
    assert response.status_code == 200
    assert response.json() == {"shape": "diamond", "times": 5, "area": 25.0}

# # ------------------- AUTHENTICATION TEST CASES -------------------

def test_invalid_credentials():
    response = client.post("/shape/rectangle?times=4", headers=auth_headers(username="wrong", password="wrong"))
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_missing_credentials():
    response = client.post("/shape/rectangle?times=4")
    print(response.status_code)
    print(response.status_code)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

# ------------------- ERROR TEST CASES -------------------

def test_invalid_shape():
    response = client.post("/shape/circle?times=4", headers=auth_headers())
    assert response.status_code == 400
    assert response.json() == {"detail": "Shape 'circle' is not supported. Please choose 'rectangle', 'triangle', or 'diamond'."}

def test_negative_times():
    response = client.post("/shape/triangle?times=-2", headers=auth_headers())
    assert response.status_code == 400
    assert response.json() == {"detail": "times must be a positive integer."}

def test_zero_times():
    response = client.post("/shape/diamond?times=0", headers=auth_headers())
    assert response.status_code == 400
    assert response.json() == {"detail": "times must be a positive integer."}

def test_missing_times_query_param():
    response = client.post("/shape/rectangle", headers=auth_headers())
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()

# ------------------- TESTING LARGE TIMES VALUE -------------------

def test_large_times_value():
    response = client.post("/shape/rectangle?times=100", headers=auth_headers())
    assert response.status_code == 200
    assert response.json() == {"shape": "rectangle", "times": 100, "area": 10000.0}
