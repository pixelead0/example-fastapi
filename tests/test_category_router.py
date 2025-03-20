import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.category.schemas import CategoryCreate, CategoryUpdate

client = TestClient(app)


def test_get_categories():
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_category():
    response = client.get("/api/categories/1")
    assert response.status_code in [200, 404]  # 404 if category not found


def test_create_category():
    category_data = CategoryCreate(name="Unique Test Category 123")
    response = client.post("/api/categories", json=category_data.model_dump())
    assert response.status_code == 201
    assert "id" in response.json()


def test_update_category():
    category_data = CategoryUpdate(name="Another Unique Category 456")
    response = client.put("/api/categories/1", json=category_data.model_dump())
    assert response.status_code in [200, 404]  # 404 if category not found


def test_delete_category():
    response = client.delete("/api/categories/1")
    assert response.status_code in [204, 404]  # 404 if category not found 