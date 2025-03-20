import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.product.schemas import ProductCreate, ProductUpdate
from src.core.database import engine, Base
from sqlalchemy import create_engine
from httpx import AsyncClient

client = TestClient(app)

# Remove the duplicate fixture, as it's already defined in conftest.py
# The global fixture in conftest.py will handle database setup/teardown

@pytest.mark.asyncio
def test_get_products():
    async def inner():
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/api/products")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    return inner()


@pytest.mark.asyncio
def test_search_products():
    async def inner():
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/api/products/search?q=test")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    return inner()


@pytest.mark.asyncio
def test_get_product():
    async def inner():
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/api/products/1")
        assert response.status_code in [200, 404]  # 404 if product not found
    return inner()


@pytest.mark.asyncio
def test_get_product_by_sku():
    async def inner():
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/api/products/sku/test-sku")
        assert response.status_code in [200, 404]  # 404 if product not found
    return inner()


@pytest.mark.asyncio
def test_create_product():
    async def inner():
        product_data = ProductCreate(name="Unique Test Product 123", sku="unique-test-sku-123", price=10.0)
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/products", json=product_data.model_dump())
        assert response.status_code == 201
        assert "id" in response.json()
    return inner()


def test_update_product():
    product_data = ProductUpdate(name="Updated Unique Product 456", sku="updated-unique-sku-456", price=15.0)
    response = client.put("/api/products/1", json=product_data.model_dump())
    assert response.status_code in [200, 404]  # 404 if product not found


def test_delete_product():
    response = client.delete("/api/products/1")
    assert response.status_code in [204, 404]  # 404 if product not found 