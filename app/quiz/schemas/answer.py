import datetime

from pydantic import BaseModel

from app.quiz.schemas import BaseSchema
from app.quiz.schemas.question import QuestionSchema


class AnswerSchema(BaseSchema):
    id: int
    text: str
    is_right: bool
    question_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class AnswerSimpleSchema(BaseSchema):
    id: int
    text: str
    is_right: bool


class CreateAnswerSchema(BaseSchema):
    text: str
    question_id: int
    is_right: bool = False


class UpdateAnswerSchema(BaseSchema):
    text: str | None = None
    is_right: bool | None = None


class QuestionAnswersSchema(BaseSchema):
    id: int
    name: str
    pack_id: int
    answers: list[AnswerSimpleSchema]
