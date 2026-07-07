from fastapi.testclient import TestClient
from app.main import app, get_db
from app.database import Base, engine
from sqlalchemy.orm import sessionmaker
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine_test = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_register():
    response = client.post("/auth/register", json={"email": "test1@example.com", "password": "password"})
    if response.status_code == 400: # Already exists from previous run
        assert response.json()["detail"] == "Email already registered"
    else:
        assert response.status_code == 201
        assert response.json()["email"] == "test1@example.com"

def test_register_duplicate():
    client.post("/auth/register", json={"email": "dup@example.com", "password": "password"})
    response = client.post("/auth/register", json={"email": "dup@example.com", "password": "password"})
    assert response.status_code == 400

def get_token(email="test1@example.com", password="password"):
    response = client.post("/auth/login", data={"username": email, "password": password})
    return response.json().get("access_token")

def test_login_success():
    response = client.post("/auth/login", data={"username": "test1@example.com", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    response = client.post("/auth/login", data={"username": "test1@example.com", "password": "wrong"})
    assert response.status_code == 401

def test_create_product_no_token():
    response = client.post("/items", json={"name": "No Token", "price": 10.0})
    assert response.status_code == 401

def test_create_product_with_token():
    token = get_token()
    response = client.post("/items", json={"name": "Token Product", "description": "Desc", "price": 10.5}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["name"] == "Token Product"
    return response.json()["id"]

def test_read_my_items():
    token = get_token()
    response = client.get("/users/me/items", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_authorization_update_delete():
    # User 1 creates product
    token1 = get_token()
    response = client.post("/items", json={"name": "Auth Product", "price": 10.0}, headers={"Authorization": f"Bearer {token1}"})
    product_id = response.json()["id"]

    # User 2 tries to update
    client.post("/auth/register", json={"email": "test2@example.com", "password": "password"})
    token2 = get_token("test2@example.com", "password")

    response2 = client.put(f"/items/{product_id}", json={"name": "Hacked", "price": 5.0}, headers={"Authorization": f"Bearer {token2}"})
    assert response2.status_code == 403
    assert response2.json()["detail"] == "You are not authorized to modify this resource."

    # User 2 tries to delete
    response3 = client.delete(f"/items/{product_id}", headers={"Authorization": f"Bearer {token2}"})
    assert response3.status_code == 403

    # User 1 deletes
    response4 = client.delete(f"/items/{product_id}", headers={"Authorization": f"Bearer {token1}"})
    assert response4.status_code == 200

def test_invalid_token():
    response = client.post("/items", json={"name": "Test", "price": 10.0}, headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
