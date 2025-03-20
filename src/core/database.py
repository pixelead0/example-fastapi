import importlib
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import Column, Integer, DateTime, func, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import select

from src.core.config import get_settings

settings = get_settings()

# Create an async engine
engine = create_async_engine('sqlite+aiosqlite:///test.db', echo=True)

# Create metadata object with naming convention
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

# Create base for models
Base = declarative_base(metadata=metadata)

# Create a session factory
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Use the session factory directly for async operations
async def get_db():
    async with async_session_factory() as session:
        yield session


class BaseModel(Base):
    """Base SQLAlchemy model with common fields."""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )


async def init_models():
    """Initialize models by creating tables."""
    async with engine.begin() as conn:
        # Import all modules with models to ensure they are registered
        importlib.import_module("src.product.models")
        importlib.import_module("src.category.models")
        importlib.import_module("src.log.models")
        
        # Drop and create all tables
        # WARNING: This will delete all data! Only use in development/testing
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all) 