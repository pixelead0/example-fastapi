from pydantic import BaseModel, Field, constr, condecimal, conint
from typing import List, Optional
from datetime import datetime

# Category schemas for references
class CategoryRef(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# Base Product Schema
class ProductBase(BaseModel):
    name: constr(min_length=3, max_length=100) = Field(..., example="Product Name")
    description: Optional[constr(max_length=500)] = Field(None, example="Product description")
    price: float = Field(..., example=19.99)
    sku: constr(min_length=3, max_length=50) = Field(..., example="PRD-12345")
    is_active: bool = Field(True, example=True)
    stock_quantity: conint(ge=0) = Field(0, example=100)


# Schema for creating a Product
class ProductCreate(ProductBase):
    category_ids: Optional[List[int]] = Field(None, example=[1, 2])


# Schema for updating a Product
class ProductUpdate(BaseModel):
    name: Optional[constr(min_length=3, max_length=100)] = Field(None, example="Updated Product Name")
    description: Optional[constr(max_length=500)] = Field(None, example="Updated product description")
    price: Optional[float] = Field(None, example=29.99)
    sku: Optional[constr(min_length=3, max_length=50)] = Field(None, example="PRD-54321")
    is_active: Optional[bool] = Field(None, example=True)
    stock_quantity: Optional[conint(ge=0)] = Field(None, example=150)
    category_ids: Optional[List[int]] = Field(None, example=[1, 3])


# Schema for Product response
class ProductResponse(ProductBase):
    id: int
    categories: List[CategoryRef] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Schema for Product list response (could be extended for pagination metadata)
class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    
    class Config:
        from_attributes = True 