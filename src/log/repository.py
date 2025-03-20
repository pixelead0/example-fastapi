from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta

from src.core.repository import BaseRepository
from src.log.models import OperationLog


class OperationLogRepository(BaseRepository[OperationLog]):
    """Repository for OperationLog model."""

    def __init__(self):
        super().__init__(OperationLog)
        
    async def log_operation(
        self,
        db: AsyncSession,
        operation_type: str,
        entity_type: str,
        entity_id: Optional[int] = None,
        user_id: Optional[int] = None,
        details: Optional[str] = None,
        status: str = "success",
        error_message: Optional[str] = None,
    ) -> OperationLog:
        """Log an operation."""
        log_data = {
            "operation_type": operation_type,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "user_id": user_id,
            "details": details,
            "status": status,
            "error_message": error_message,
        }
        return await self.add(db, log_data)
        
    async def get_logs_by_entity(
        self,
        db: AsyncSession,
        entity_type: str,
        entity_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[OperationLog]:
        """Get logs for a specific entity."""
        query = (
            select(self.model)
            .where(
                self.model.entity_type == entity_type,
                self.model.entity_id == entity_id
            )
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
        
    async def get_logs_by_type(
        self,
        db: AsyncSession,
        operation_type: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[OperationLog]:
        """Get logs for a specific operation type."""
        query = (
            select(self.model)
            .where(self.model.operation_type == operation_type)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
        
    async def get_error_logs(
        self,
        db: AsyncSession,
        since: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[OperationLog]:
        """Get error logs."""
        if not since:
            # Default to last 24 hours
            since = datetime.now() - timedelta(days=1)
            
        query = (
            select(self.model)
            .where(
                self.model.status == "error",
                self.model.created_at >= since
            )
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all() 