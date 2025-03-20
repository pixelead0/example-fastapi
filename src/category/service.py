from typing import Dict, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.category.repository import CategoryRepository
from src.category.exceptions import CategoryNotFoundException, CategoryConflictException
from src.category.models import Category
from src.log.repository import OperationLogRepository


class CategoryService:
    def __init__(self):
        self.category_repo = CategoryRepository()
        self.log_repo = OperationLogRepository()
    
    async def get_categories(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Category]:
        """Get all categories with pagination."""
        return await self.category_repo.get_all(db, skip=skip, limit=limit)
    
    async def get_category(self, db: AsyncSession, category_id: int) -> Category:
        """Get a category by ID."""
        category = await self.category_repo.get_by_id(db, category_id)
        if not category:
            await self.log_repo.log_operation(
                db, 
                "READ", 
                "Category", 
                str(category_id), 
                "system", 
                f"Attempted to retrieve non-existent category with ID {category_id}",
                "ERROR",
                "Category not found"
            )
            raise CategoryNotFoundException()
        
        await self.log_repo.log_operation(
            db, 
            "READ", 
            "Category", 
            str(category_id), 
            "system", 
            f"Retrieved category with ID {category_id}",
            "SUCCESS"
        )
        return category
    
    async def get_category_by_name(self, db: AsyncSession, name: str) -> Optional[Category]:
        """Get a category by name."""
        return await self.category_repo.get_by_name(db, name)
    
    async def create_category(self, db: AsyncSession, category_data: Dict[str, Any]) -> Category:
        """Create a new category."""
        # Check if category with same name already exists
        existing_category = await self.category_repo.get_by_name(db, category_data["name"])
        if existing_category:
            await self.log_repo.log_operation(
                db, 
                "CREATE", 
                "Category", 
                category_data["name"], 
                "system", 
                f"Attempted to create category with existing name '{category_data['name']}'",
                "ERROR",
                "Category with this name already exists"
            )
            raise CategoryConflictException("Category with this name already exists")
        
        # Create the category
        category = await self.category_repo.add(db, category_data)
        
        await self.log_repo.log_operation(
            db, 
            "CREATE", 
            "Category", 
            str(category.id), 
            "system", 
            f"Created new category with ID {category.id} and name '{category.name}'",
            "SUCCESS"
        )
        
        return category
    
    async def update_category(self, db: AsyncSession, category_id: int, update_data: Dict[str, Any]) -> Category:
        """Update an existing category."""
        # Check if category exists
        category = await self.category_repo.get_by_id(db, category_id)
        if not category:
            await self.log_repo.log_operation(
                db, 
                "UPDATE", 
                "Category", 
                str(category_id), 
                "system", 
                f"Attempted to update non-existent category with ID {category_id}",
                "ERROR",
                "Category not found"
            )
            raise CategoryNotFoundException()
        
        # If name is being changed, check it doesn't conflict
        if "name" in update_data and update_data["name"] != category.name:
            existing_category = await self.category_repo.get_by_name(db, update_data["name"])
            if existing_category and existing_category.id != category_id:
                await self.log_repo.log_operation(
                    db, 
                    "UPDATE", 
                    "Category", 
                    str(category_id), 
                    "system", 
                    f"Attempted to update category with conflicting name '{update_data['name']}'",
                    "ERROR",
                    "Another category with this name already exists"
                )
                raise CategoryConflictException("Another category with this name already exists")
        
        # Update category data
        updated_category = await self.category_repo.update(db, category_id, update_data)
        
        await self.log_repo.log_operation(
            db, 
            "UPDATE", 
            "Category", 
            str(category_id), 
            "system", 
            f"Updated category with ID {category_id}",
            "SUCCESS"
        )
        
        return updated_category
    
    async def delete_category(self, db: AsyncSession, category_id: int) -> bool:
        """Delete a category."""
        # Check if category exists
        category = await self.category_repo.get_by_id(db, category_id)
        if not category:
            await self.log_repo.log_operation(
                db, 
                "DELETE", 
                "Category", 
                str(category_id), 
                "system", 
                f"Attempted to delete non-existent category with ID {category_id}",
                "ERROR",
                "Category not found"
            )
            raise CategoryNotFoundException()
        
        # Delete the category
        success = await self.category_repo.delete(db, category_id)
        
        if success:
            await self.log_repo.log_operation(
                db, 
                "DELETE", 
                "Category", 
                str(category_id), 
                "system", 
                f"Deleted category with ID {category_id}",
                "SUCCESS"
            )
        else:
            await self.log_repo.log_operation(
                db, 
                "DELETE", 
                "Category", 
                str(category_id), 
                "system", 
                f"Failed to delete category with ID {category_id}",
                "ERROR",
                "Database error during deletion"
            )
        
        return success 