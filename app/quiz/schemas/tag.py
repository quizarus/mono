
from app.quiz.schemas import BaseSchema


class TagSchema(BaseSchema):
    id: int
    name: str


class CreateTagSchema(BaseSchema):
    name: str


class UpdateTagSchema(BaseSchema):
    name: str


