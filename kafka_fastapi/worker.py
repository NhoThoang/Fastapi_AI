from confluent_kafka import Consumer, Producer
import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient("localhost", port=6333)
producer = Producer({'bootstrap.servers': 'localhost:9092'})

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'worker-group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(["question-topic"])

def fake_generate(context, question):
    return f"Câu trả lời cho: '{question}' với ngữ cảnh: '{context}'"

while True:
    msg = consumer.poll(1.0)
    if msg is None: continue
    data = json.loads(msg.value().decode("utf-8"))

    vector = model.encode(data["text"]).tolist()
    results = qdrant.search(
        collection_name="my_collection",
        query_vector=vector,
        limit=3
    )
    context = " ".join([r.payload["text"] for r in results])
    answer = fake_generate(context, data["text"])

    result = {
        "id": data["id"],
        "answer": answer
    }
    producer.produce("answer-topic", json.dumps(result).encode("utf-8"))
    producer.flush()

    # consumer.commit(msg)