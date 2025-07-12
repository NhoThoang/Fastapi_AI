from fastapi import FastAPI
from uuid import uuid4
from schemas import QuestionRequest, AnswerResponse
from kafka_client import send_question_to_kafka, listen_for_answer

app = FastAPI()

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(question: QuestionRequest):
    req_id = str(uuid4())
    data = {
        "id": req_id,
        "text": question.text,
        "user_id": question.user_id
    }

    send_question_to_kafka(data)

    # Chờ worker trả kết quả qua Kafka
    result = listen_for_answer(req_id)
    if result:
        return AnswerResponse(
            question=question.text,
            answer=result["answer"],
            user_id=question.user_id
        )
    return {"question": question.text, "answer": "Không có phản hồi từ hệ thống."}
