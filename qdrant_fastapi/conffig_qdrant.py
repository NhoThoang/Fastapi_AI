from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance, VectorParams,
    PointStruct, OptimizersConfigDiff, HnswConfigDiff
)
from sentence_transformers import SentenceTransformer
import uuid

app = FastAPI()

# ⚙️ Embedding model (768 chiều)
model = SentenceTransformer("all-mpnet-base-v2")  # hoặc "bge-base-en-v1.5"
VECTOR_SIZE = model.get_sentence_embedding_dimension()
COLLECTION_NAME = "my_collection"

# ⚙️ Qdrant async client
client = AsyncQdrantClient(host="localhost", port=6333)

# ✅ Khởi tạo collection với config tối ưu
@app.on_event("startup")
async def startup_event():
    await client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        ),
        optimizers_config=OptimizersConfigDiff(
            default_segment_number=4,
            max_segment_size=50000
        ),
        hnsw_config=HnswConfigDiff(
            m=16,
            ef_construct=256,
            full_scan_threshold=1000000
        )
    )

@app.on_event("shutdown")
async def shutdown_event():
    await client.close()

# ✅ Schema gửi lên từ client
class TextInsert(BaseModel):
    text: str
    metadata: Optional[dict] = {}

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

# ✅ Search text tương tự
class SearchQuery(BaseModel):
    query: str
    top_k: int = 3

@app.post("/search-text")
async def search_text(query: SearchQuery):
    query_vector = model.encode(query.query).tolist()

    result = await client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=query.top_k,
        search_params={"ef": 128}  # tăng độ chính xác
    )

    return [
        {
            "score": hit.score,
            "payload": hit.payload
        }
        for hit in result
    ]
