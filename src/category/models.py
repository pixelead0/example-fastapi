from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from src.core.database import BaseModel


class Category(BaseModel):
    """Category model for grouping products."""
    
    __tablename__ = "categories"
    
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    products = relationship("Product", secondary="product_categories", back_populates="categories")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')" 