from fastapi import APIRouter, Depends, Path, Query, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.category.schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from src.category.service import CategoryService
from src.category.exceptions import CategoryNotFoundException, CategoryConflictException

router = APIRouter(prefix="/categories", tags=["Categories"])
service = CategoryService()


@router.get("", response_model=List[CategoryResponse])
async def get_categories(
    skip: int = Query(0, ge=0, description="Skip N categories"),
    limit: int = Query(100, ge=1, le=100, description="Limit to N categories"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all categories with pagination.
    """
    return await service.get_categories(db, skip=skip, limit=limit)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int = Path(..., gt=0, description="Category ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a category by ID.
    """
    try:
        return await service.get_category(db, category_id)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new category.
    """
    try:
        return await service.create_category(db, category.model_dump())
    except CategoryConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category: CategoryUpdate,
    category_id: int = Path(..., gt=0, description="Category ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing category.
    """
    try:
        return await service.update_category(db, category_id, category.model_dump(exclude_unset=True))
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CategoryConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int = Path(..., gt=0, description="Category ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a category.
    """
    try:
        result = await service.delete_category(db, category_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Failed to delete category"
            )
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) 