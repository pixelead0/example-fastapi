from typing import List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from sqlalchemy.orm import selectinload

from src.core.repository import BaseRepository
from src.product.models import Product, ProductCategory
from src.category.models import Category


class ProductRepository(BaseRepository[Product]):
    """Repository for Product model."""

    def __init__(self):
        super().__init__(Product)

    async def get_by_sku(self, db: AsyncSession, sku: str) -> Optional[Product]:
        """Get a product by SKU."""
        query = select(self.model).where(self.model.sku == sku).options(selectinload(self.model.categories))
        result = await db.execute(query)
        return result.scalars().first()

    async def search_products(
        self, 
        db: AsyncSession, 
        search_term: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Product]:
        """Search products by name or SKU."""
        search_pattern = f"%{search_term}%"
        query = (
            select(self.model)
            .where(
                or_(
                    self.model.name.ilike(search_pattern),
                    self.model.sku.ilike(search_pattern)
                )
            )
            .options(selectinload(self.model.categories))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def add_category_to_product(
        self, 
        db: AsyncSession, 
        product_id: int, 
        category_id: int
    ) -> bool:
        """Add a category to a product."""
        # Check if the association already exists
        query = (
            select(ProductCategory)
            .where(
                ProductCategory.product_id == product_id,
                ProductCategory.category_id == category_id
            )
        )
        result = await db.execute(query)
        if result.scalars().first():
            return False  # Association already exists
            
        # Create new association
        db_obj = ProductCategory(product_id=product_id, category_id=category_id)
        db.add(db_obj)
        await db.flush()
        return True

    async def remove_category_from_product(
        self, 
        db: AsyncSession, 
        product_id: int, 
        category_id: int
    ) -> bool:
        """Remove a category from a product."""
        query = (
            select(ProductCategory)
            .where(
                ProductCategory.product_id == product_id,
                ProductCategory.category_id == category_id
            )
        )
        result = await db.execute(query)
        association = result.scalars().first()
        
        if not association:
            return False  # Association doesn't exist
            
        await db.delete(association)
        await db.flush()
        return True

    async def update_product_categories(
        self, 
        db: AsyncSession, 
        product_id: int, 
        category_ids: List[int]
    ) -> Product:
        """Update all categories for a product."""
        # Get current associations
        query = (
            select(ProductCategory)
            .where(ProductCategory.product_id == product_id)
        )
        result = await db.execute(query)
        current_associations = result.scalars().all()
        
        # Get current category IDs
        current_category_ids = {assoc.category_id for assoc in current_associations}
        
        # Categories to add
        for cat_id in category_ids:
            if cat_id not in current_category_ids:
                await self.add_category_to_product(db, product_id, cat_id)
                
        # Categories to remove
        for assoc in current_associations:
            if assoc.category_id not in category_ids:
                await db.delete(assoc)
                
        await db.flush()
        
        # Return updated product
        return await self.get_by_id(db, product_id, load_relations=["categories"])

    async def get_by_id(self, db: AsyncSession, id: int, load_relations: Optional[List[Any]] = None) -> Optional[Product]:
        """Get a product by ID with optional eager loading of relationships."""
        query = select(self.model).where(self.model.id == id)
        if load_relations:
            for relation in load_relations:
                query = query.options(selectinload(getattr(self.model, relation)))
        result = await db.execute(query)
        return result.scalars().first() 