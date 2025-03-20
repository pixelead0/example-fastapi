from sqlalchemy import Column, String, Text, Integer

from src.core.database import BaseModel


class OperationLog(BaseModel):
    """Log for tracking operations."""
    
    __tablename__ = "operation_logs"
    
    operation_type = Column(String(50), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="success")
    error_message = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<OperationLog(id={self.id}, type='{self.operation_type}', entity='{self.entity_type}', status='{self.status}')>" 