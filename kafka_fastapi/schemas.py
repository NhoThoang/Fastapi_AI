from pydantic import BaseModel
from typing import Optional

class QuestionRequest(BaseModel):
    text: str
    user_id: Optional[str] = None

class AnswerResponse(BaseModel):
    question: str
    answer: str
    user_id: Optional[str] = None
