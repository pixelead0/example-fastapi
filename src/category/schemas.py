from pydantic import BaseModel, Field, constr
from typing import List, Optional
from datetime import datetime


# Base Category Schema
class CategoryBase(BaseModel):
    name: constr(min_length=2, max_length=50) = Field(..., example="Electronics")
    description: Optional[constr(max_length=200)] = Field(None, example="Electronic products and gadgets")


# Schema for creating a Category
class CategoryCreate(CategoryBase):
    pass


# Schema for updating a Category
class CategoryUpdate(BaseModel):
    name: Optional[constr(min_length=2, max_length=50)] = Field(None, example="Updated Electronics")
    description: Optional[constr(max_length=200)] = Field(None, example="Updated description for electronic products")


# Schema for Category response
class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Schema for Category list response (could be extended for pagination metadata)
class CategoryListResponse(BaseModel):
    items: List[CategoryResponse]
    total: int
    
    class Config:
        from_attributes = True 