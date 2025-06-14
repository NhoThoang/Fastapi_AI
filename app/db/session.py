from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import ConfigDB

async_engine = create_async_engine(
    ConfigDB.SQLALCHEMY_DATABASE_URI,
    pool_size=ConfigDB.SQLALCHEMY_POOL_SIZE,
    max_overflow=ConfigDB.SQLALCHEMY_MAX_OVERFLOW,
    pool_recycle=ConfigDB.SQLALCHEMY_POOL_RECYCLE,
    pool_timeout=ConfigDB.SQLALCHEMY_POOL_TIMEOUT,
    echo=ConfigDB.SQLALCHEMY_ECHO
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
