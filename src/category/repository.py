from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.repository import BaseRepository
from src.category.models import Category


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category model."""

    def __init__(self):
        super().__init__(Category)

    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Category]:
        """Get a category by name."""
        query = select(self.model).where(self.model.name == name)
        result = await db.execute(query)
        return result.scalars().first() 