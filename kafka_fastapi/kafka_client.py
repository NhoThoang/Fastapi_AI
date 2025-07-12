from confluent_kafka import Producer, Consumer
import json

KAFKA_BOOTSTRAP = "localhost:9092"
QUESTION_TOPIC = "question-topic"
ANSWER_TOPIC = "answer-topic"

producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP})

def send_question_to_kafka(data: dict):
    producer.produce(QUESTION_TOPIC, json.dumps(data).encode("utf-8"))
    producer.flush()

def listen_for_answer(request_id: str, timeout=10):
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP,
        'group.id': 'fastapi-consumer',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([ANSWER_TOPIC])

    import time
    start = time.time()
    while time.time() - start < timeout:
        msg = consumer.poll(1.0)
        if msg is None: continue
        payload = json.loads(msg.value().decode("utf-8"))
        if payload.get("id") == request_id:
            consumer.close()
            return payload
    consumer.close()
    return None
