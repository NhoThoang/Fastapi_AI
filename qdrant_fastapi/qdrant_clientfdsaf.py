import aiohttp
from qdrant_client.async_qdrant_client import AsyncQdrantClient

# Connection pool config
connector = aiohttp.TCPConnector(limit=100)  # Tối đa 100 kết nối

# Khởi tạo aiohttp session có pool
session = aiohttp.ClientSession(connector=connector)

# Tạo client Qdrant dùng session
qdrant_client = AsyncQdrantClient(
    host="localhost",
    port=6333,
    aiohttp_session=session
)
