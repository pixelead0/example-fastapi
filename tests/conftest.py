import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import engine, Base

@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Drop tables after tests
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) 