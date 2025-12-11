import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from backend.app.data_base.database import Base, get_async_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(scope="function")
async def async_db():
    engine = create_async_engine(TEST_DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)