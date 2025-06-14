# import asyncio
# from app.db.session import async_engine
# from app.db.base import Base
# from app.models import Account, Products  # Đảm bảo model được import

# async def init_db():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# if __name__ == "__main__":
#     asyncio.run(init_db())

import asyncio
from app.db.session import async_engine
from app.models import Account, Products, user_devices
from app.db.base import Base

async def init_db():
    async with async_engine.begin() as conn:
        print("🔨 Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Done.")

if __name__ == "__main__":
    asyncio.run(init_db())
