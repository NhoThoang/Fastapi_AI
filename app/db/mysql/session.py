from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import config_db

async_engine = create_async_engine(
    config_db.sqlalchemy_database_uri,
    pool_size=config_db.sqlalchemy_pool_size,
    max_overflow=config_db.sqlalchemy_max_overflow,
    pool_recycle=config_db.sqlalchemy_pool_recycle,
    pool_timeout=config_db,
    echo=config_db.sqlalchemy_echo
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
