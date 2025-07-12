from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
import uuid

app = FastAPI()

# ✅ Khởi tạo embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")  # hoặc bất kỳ model nào bạn thích

# ✅ Qdrant client async
client = AsyncQdrantClient(host="localhost", port=6333)

# ✅ Collection name và vector size
COLLECTION_NAME = "my_collection"
VECTOR_SIZE = model.get_sentence_embedding_dimension()

# ✅ Tạo collection khi khởi động
@app.on_event("startup")
async def startup_event():
    await client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
    )

@app.on_event("shutdown")
async def shutdown_event():
    await client.close()

# ✅ Schema: text input từ người dùng
class TextInsert(BaseModel):
    text: str
    metadata: Optional[dict] = {}  # lưu kèm metadata như file name, page,...

# ✅ API: người dùng gửi text → server embed + lưu vector
@app.post("/insert-text")
async def insert_text(data: TextInsert):
    vector = model.encode(data.text).tolist()
    point_id = str(uuid.uuid4())

    await client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "text": data.text,
                    **data.metadata
                }
            )
        ]
    )
    return {"status": "inserted", "id": point_id}

# ✅ API: tìm text gần nhất
class SearchQuery(BaseModel):
    query: str
    top_k: int = 3

@app.post("/search-text")
async def search_text(query: SearchQuery):
    query_vector = model.encode(query.query).tolist()

    result = await client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=query.top_k
    )

    return [
        {
            "score": hit.score,
            "payload": hit.payload
        }
        for hit in result
    ]
