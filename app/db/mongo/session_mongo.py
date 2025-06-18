# database.py
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
# from app.schemas.mongo_model import User
from app.models.mongo.product_detail import ProductDetail
from app.core.config import mongo_settings

def get_mongo_client():
    return AsyncIOMotorClient(
        mongo_settings.mongo_uri,
        maxPoolSize=mongo_settings.max_pool_size,
        minPoolSize=mongo_settings.min_pool_size,
        connectTimeoutMS=mongo_settings.connect_timeout_ms,
        serverSelectionTimeoutMS=mongo_settings.server_selection_timeout_ms,
        socketTimeoutMS=mongo_settings.socket_timeout_ms,
        waitQueueTimeoutMS=mongo_settings.wait_queue_timeout_ms,
        retryWrites=mongo_settings.retry_writes,
        w=mongo_settings.write_concern,
        journal=mongo_settings.journal,
        tz_aware=mongo_settings.tz_aware,
    )

async def init_db():
    client = get_mongo_client()
    db = client[mongo_settings.db_name]
    await init_beanie(database=db, document_models=[ProductDetail])


    
# async def get_mongo_db():
#     client = get_mongo_client()
#     db = client["my_fastapi_app"]
#     try:
#         yield db
#     finally:
#         client.close()

# def get_mongo_collection(collection_name: str):
#     client = get_mongo_client()
#     db = client["my_fastapi_app"]
#     return db[collection_name]
# async def get_mongo_collection_async(collection_name: str):
#     client = get_mongo_client()
#     db = client["my_fastapi_app"]
#     collection = db[collection_name]
#     try:
#         yield collection
#     finally:
#         client.close()

# This function is used to get a MongoDB collection asynchronously.
# It creates a MongoDB client, accesses the specified database and collection,
# and yields the collection for use in the application.
# After the operation is done, it ensures that the client is closed properly.
# async def test_get_products(db: AsyncIOMotorClient):
#     collection = db["products"]
#     products = await collection.find().to_list(length=None)
#     return products
# async def get_refresh_token(db: AsyncIOMotorClient, username: str) -> Optional[str]:
#     doc = await db["accounts"].find_one(
#         {"username": username},
#         {"_id": 0, "refresh_token": 1}  # chỉ lấy refresh_token
#     )
#     return doc["refresh_token"] if doc else None