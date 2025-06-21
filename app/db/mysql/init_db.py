import asyncio
from app.db.mysql.session import async_engine
from app.models import Account, Products, Product_images
from app.models.mysql import user_devices
from app.db.mysql.base import Base

async def init_db():
    async with async_engine.begin() as conn:
        print("🔨 Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Done.")

if __name__ == "__main__":
    asyncio.run(init_db())
