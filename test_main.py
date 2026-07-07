from fastapi.testclient import TestClient
from app.main import app, get_db
from app.database import Base, engine
from sqlalchemy.orm import sessionmaker
import pytest

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine_test = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_product():
    response = client.post("/items", json={"name": "Test Product", "description": "A test product", "price": 10.5})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 10.5
    assert "id" in data
    return data["id"]

def test_create_product_validation_error():
    # empty name
    response = client.post("/items", json={"name": "", "price": 10.5})
    assert response.status_code == 422
    # price <= 0
    response = client.post("/items", json={"name": "Test", "price": 0})
    assert response.status_code == 422

def test_read_products():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_product():
    product_id = test_create_product()
    response = client.get(f"/items/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id

def test_read_non_existing_product():
    response = client.get("/items/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_update_product():
    product_id = test_create_product()
    response = client.put(f"/items/{product_id}", json={"name": "Updated Name", "price": 20.0})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["price"] == 20.0

def test_delete_product():
    product_id = test_create_product()
    response = client.delete(f"/items/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Product deleted"}
    
    # Verify deletion
    response2 = client.get(f"/items/{product_id}")
    assert response2.status_code == 404

def test_delete_non_existing_product():
    response = client.delete("/items/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_swagger_ui_loads():
    response = client.get("/docs")
    assert response.status_code == 200
