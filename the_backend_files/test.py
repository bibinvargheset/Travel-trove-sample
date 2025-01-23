#this area is for testing nothing usefull here really


""""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user import app, get_db  # Assuming your main file is named user.py
from main import engine
from models import Base

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the dependency to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create a TestClient instance
client = TestClient(app)

# Test database initialization (run migrations or create tables as needed)
def setup_module(module):
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
    Base.metadata.drop_all(bind=engine)

# Define test cases
def test_register_user():
    response = client.post(
        "/register/",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "profile_id": 1
        }
    )


      assert response.status_code == 200
    # data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"

def test_register_user_existing_username():
    response = client.post(
        "/register/",
        json={
            "username": "testuser",
            "email": "newemail@example.com",
            "password": "password123",
            "profile_id": 2
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Username already registered"

def test_register_user_existing_email():
    response = client.post(
        "/register/",
        json={
            "username": "newuser",
            "email": "testuser@example.com",
            "password": "password123",
            "profile_id": 3
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Email already registered"

def test_get_user():
    response = client.get("/user/1")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"

def test_get_non_existent_user():
    response = client.get("/user/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"

# Commenting out image-related test cases
# def test_update_profile_pic():
#     with open("test_profile.jpg", "rb") as file:
#         response = client.put(
#             "/user/1/profile",
#             files={"profile_pic": file}
#         )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["username"] == "testuser"

# def test_get_profile_pic():
#     response = client.get("/user/1/profile")
#     assert response.status_code == 200
#     assert response.headers["content-type"] == "image/jpeg"

# def test_update_profile_pic_non_existent_user():
#     with open("test_profile.jpg", "rb") as file:
#         response = client.put(
#             "/user/999/profile",
#             files={"profile_pic": file}
#         )
#     assert response.status_code == 404
#     data = response.json()
#     assert data["detail"] == "User not found"

# def test_get_profile_pic_non_existent_user():
#     response = client.get("/user/999/profile")
#     assert response.status_code == 404
#     data = response.json()
#     assert data["detail"] == "User not found"
"""