from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AnswerOut(BaseModel):
    id: int
    answer_text: str

    model_config = ConfigDict(from_attributes=True)


class QuestionOut(BaseModel):
    id: int
    question_text: str
    question_type: str
    image_url: str | None = None
    difficulty: str | None = None
    answers: list[AnswerOut] = []

    model_config = ConfigDict(from_attributes=True)


class SubmitItem(BaseModel):
    question_id: int
    selected_answer_ids: list[int]


class QuizSubmit(BaseModel):
    answers: list[SubmitItem]


class QuizResultOut(BaseModel):
    id: int
    score: int
    max_score: int
    level: str | None = None
    completed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class LeaderboardEntry(BaseModel):
    user_name: str
    score: int
    max_score: int
    level: str | None = None
    completed_at: datetime | None = None
