from typing import Dict, List, Optional, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import Base
from src.product.repository import ProductRepository
from src.product.exceptions import ProductNotFoundException, ProductConflictException
from src.product.models import Product
from src.category.models import Category
from src.category.repository import CategoryRepository
from src.log.repository import OperationLogRepository


class ProductService:
    def __init__(self):
        self.product_repo = ProductRepository()
        self.category_repo = CategoryRepository()
        self.log_repo = OperationLogRepository()
    
    async def get_products(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get all products with pagination."""
        return await self.product_repo.get_all(db, skip=skip, limit=limit)
    
    async def get_product(self, db: AsyncSession, product_id: int) -> Product:
        """Get a product by ID."""
        product = await self.product_repo.get_by_id(db, product_id)
        if not product:
            await self.log_repo.log_operation(
                db, 
                "READ", 
                "Product", 
                str(product_id), 
                "system", 
                f"Attempted to retrieve non-existent product with ID {product_id}",
                "ERROR",
                "Product not found"
            )
            raise ProductNotFoundException()
        
        await self.log_repo.log_operation(
            db, 
            "READ", 
            "Product", 
            str(product_id), 
            "system", 
            f"Retrieved product with ID {product_id}",
            "SUCCESS"
        )
        return product
    
    async def get_product_by_sku(self, db: AsyncSession, sku: str) -> Product:
        """Get a product by SKU."""
        product = await self.product_repo.get_by_sku(db, sku)
        if not product:
            await self.log_repo.log_operation(
                db, 
                "READ", 
                "Product", 
                sku, 
                "system", 
                f"Attempted to retrieve non-existent product with SKU {sku}",
                "ERROR",
                "Product not found"
            )
            raise ProductNotFoundException()
        
        await self.log_repo.log_operation(
            db, 
            "READ", 
            "Product", 
            sku, 
            "system", 
            f"Retrieved product with SKU {sku}",
            "SUCCESS"
        )
        return product
    
    async def search_products(self, db: AsyncSession, search_term: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Search products by name or SKU."""
        return await self.product_repo.search_products(db, search_term, skip=skip, limit=limit)
    
    async def create_product(self, db: AsyncSession, product_data: Dict[str, Any]) -> Product:
        """Create a new product."""
        # Check if product with same SKU already exists
        existing_product = await self.product_repo.get_by_sku(db, product_data["sku"])
        if existing_product:
            await self.log_repo.log_operation(
                db, 
                "CREATE", 
                "Product", 
                product_data["sku"], 
                "system", 
                f"Attempted to create product with existing SKU {product_data['sku']}",
                "ERROR",
                "Product with this SKU already exists"
            )
            raise ProductConflictException("Product with this SKU already exists")
        
        # Extract category IDs if present
        category_ids = product_data.pop("category_ids", None)
        
        # Create the product
        product = await self.product_repo.add(db, product_data)
        
        # Add categories if provided
        if category_ids:
            for cat_id in category_ids:
                category = await self.category_repo.get_by_id(db, cat_id)
                if category:
                    await self.product_repo.add_category_to_product(db, product.id, cat_id)
        
        # Instead of using load_relations, directly get the product with categories
        # This ensures the categories are loaded in the current async context
        product = await self.product_repo.get_by_sku(db, product.sku)
        
        await self.log_repo.log_operation(
            db, 
            "CREATE", 
            "Product", 
            str(product.id), 
            "system", 
            f"Created new product with ID {product.id} and SKU {product.sku}",
            "SUCCESS"
        )
        
        return product
    
    async def update_product(self, db: AsyncSession, product_id: int, update_data: Dict[str, Any]) -> Product:
        """Update an existing product."""
        # Check if product exists
        product = await self.product_repo.get_by_id(db, product_id)
        if not product:
            await self.log_repo.log_operation(
                db, 
                "UPDATE", 
                "Product", 
                str(product_id), 
                "system", 
                f"Attempted to update non-existent product with ID {product_id}",
                "ERROR",
                "Product not found"
            )
            raise ProductNotFoundException()
        
        # If SKU is being changed, check it doesn't conflict
        if "sku" in update_data and update_data["sku"] != product.sku:
            existing_product = await self.product_repo.get_by_sku(db, update_data["sku"])
            if existing_product and existing_product.id != product_id:
                await self.log_repo.log_operation(
                    db, 
                    "UPDATE", 
                    "Product", 
                    str(product_id), 
                    "system", 
                    f"Attempted to update product with conflicting SKU {update_data['sku']}",
                    "ERROR",
                    "Another product with this SKU already exists"
                )
                raise ProductConflictException("Another product with this SKU already exists")
        
        # Extract category IDs if present
        category_ids = update_data.pop("category_ids", None)
        
        # Update product data
        updated_product = await self.product_repo.update(db, product_id, update_data)
        
        # Update categories if provided
        if category_ids is not None:
            await self.product_repo.update_product_categories(db, product_id, category_ids)
        
        await db.refresh(updated_product)
        
        await self.log_repo.log_operation(
            db, 
            "UPDATE", 
            "Product", 
            str(product_id), 
            "system", 
            f"Updated product with ID {product_id}",
            "SUCCESS"
        )
        
        return updated_product
    
    async def delete_product(self, db: AsyncSession, product_id: int) -> bool:
        """Delete a product."""
        # Check if product exists
        product = await self.product_repo.get_by_id(db, product_id)
        if not product:
            await self.log_repo.log_operation(
                db, 
                "DELETE", 
                "Product", 
                str(product_id), 
                "system", 
                f"Attempted to delete non-existent product with ID {product_id}",
                "ERROR",
                "Product not found"
            )
            raise ProductNotFoundException()
        
        # Delete the product
        success = await self.product_repo.delete(db, product_id)
        
        if success:
            await self.log_repo.log_operation(
                db, 
                "DELETE", 
                "Product", 
                str(product_id), 
                "system", 
                f"Deleted product with ID {product_id}",
                "SUCCESS"
            )
        else:
            await self.log_repo.log_operation(
                db, 
                "DELETE", 
                "Product", 
                str(product_id), 
                "system", 
                f"Failed to delete product with ID {product_id}",
                "ERROR",
                "Database error during deletion"
            )
        
        return success 