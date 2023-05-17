import datetime
from pydantic import BaseModel

from app.quiz.schemas import BaseSchema
from app.quiz.schemas.pack import PackSchema
from app.quiz.schemas.tag import TagSchema


class QuestionSchema(BaseSchema):
    id: int
    name: str
    description: str | None = None
    pack: PackSchema
    tags: list[TagSchema] = []
    created_at: datetime.datetime
    updated_at: datetime.datetime


class QuestionSimpleSchema(BaseSchema):
    id: int
    name: str


class CreateQuestionSchema(BaseSchema):
    name: str
    pack_id: int
    description: str | None = None
    tags: list[int] = []


class UpdateQuestionSchema(BaseSchema):
    name: str | None = None
    description: str | None = None
    tags: list[int] = []


class PackQuestionsSchema(PackSchema):
    questions: list[QuestionSimpleSchema]
