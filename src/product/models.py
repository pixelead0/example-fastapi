from sqlalchemy import Column, String, Text, Float, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.core.database import BaseModel


class Product(BaseModel):
    """Product model for storing product information."""
    
    __tablename__ = "products"
    
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    sku = Column(String(50), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    
    # Relationships
    categories = relationship("Category", secondary="product_categories", back_populates="products")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}')>"


class ProductCategory(BaseModel):
    """Product-Category association model."""
    
    __tablename__ = "product_categories"
    
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True) 