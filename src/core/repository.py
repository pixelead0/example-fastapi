from typing import TypeVar, Generic, List, Dict, Any, Optional, Type, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.sql import Select
from sqlalchemy.orm import selectinload

from src.core.database import Base

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    """
    Generic repository with common database operations.
    """
    
    def __init__(self, model: Type[T] = None):
        self.model = model
    
    async def get_by_id(self, db: AsyncSession, id: int, load_relations: Optional[List[Any]] = None) -> Optional[T]:
        """Get an entity by ID with optional eager loading of relationships."""
        query = select(self.model).where(self.model.id == id)
        if load_relations:
            for relation in load_relations:
                query = query.options(selectinload(getattr(self.model, relation)))
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination."""
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def add(self, db: AsyncSession, data: Dict[str, Any]) -> T:
        """Add a new entity."""
        db_obj = self.model(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, id: int, data: Dict[str, Any]) -> T:
        """Update an existing entity."""
        # First get the entity
        db_obj = await self.get_by_id(db, id)
        
        if db_obj:
            # Update only the fields that are present in the data
            for key, value in data.items():
                if hasattr(db_obj, key):
                    setattr(db_obj, key, value)
            
            await db.commit()
            await db.refresh(db_obj)
        
        return db_obj
    
    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Delete an entity by ID."""
        db_obj = await self.get_by_id(db, id)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
            return True
        return False
    
    async def exists(self, db: AsyncSession, id: int) -> bool:
        """Check if an entity exists by ID."""
        query = select(self.model.id).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalar() is not None
    
    async def count(self, db: AsyncSession) -> int:
        """Count all entities."""
        query = select(self.model.id)
        result = await db.execute(query)
        return len(result.all())
    
    async def execute_query(self, db: AsyncSession, query: Select) -> List[T]:
        """Execute a custom query."""
        result = await db.execute(query)
        return result.scalars().all() 