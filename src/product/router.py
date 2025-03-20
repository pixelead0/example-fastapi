from fastapi import APIRouter, Depends, Path, Query, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.product.models import Product
from src.product.schemas import (
    ProductCreate, 
    ProductUpdate, 
    ProductResponse,
    ProductListResponse
)
from src.product.service import ProductService
from src.product.exceptions import ProductNotFoundException, ProductConflictException

router = APIRouter(prefix="/products", tags=["Products"])
service = ProductService()


@router.get("", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0, description="Skip N products"),
    limit: int = Query(100, ge=1, le=100, description="Limit to N products"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all products with pagination.
    """
    return await service.get_products(db, skip=skip, limit=limit)


@router.get("/search", response_model=List[ProductResponse])
async def search_products(
    q: str = Query(..., min_length=2, description="Search term"),
    skip: int = Query(0, ge=0, description="Skip N products"),
    limit: int = Query(100, ge=1, le=100, description="Limit to N products"),
    db: AsyncSession = Depends(get_db)
):
    """
    Search products by name or SKU.
    """
    return await service.search_products(db, q, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int = Path(..., gt=0, description="Product ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a product by ID.
    """
    try:
        return await service.get_product(db, product_id)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/sku/{sku}", response_model=ProductResponse)
async def get_product_by_sku(
    sku: str = Path(..., min_length=3, max_length=50, description="Product SKU"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a product by SKU.
    """
    try:
        return await service.get_product_by_sku(db, sku)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new product.
    """
    try:
        return await service.create_product(db, product.model_dump())
    except ProductConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product: ProductUpdate,
    product_id: int = Path(..., gt=0, description="Product ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing product.
    """
    try:
        return await service.update_product(db, product_id, product.model_dump(exclude_unset=True))
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProductConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int = Path(..., gt=0, description="Product ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a product.
    """
    try:
        result = await service.delete_product(db, product_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete product")
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) 