import datetime

from pydantic import BaseModel

from app.quiz.schemas import BaseSchema
from app.quiz.schemas.tag import TagSchema


class PackSchema(BaseSchema):
    id: int
    name: str
    description: str | None = None
    tags: list[TagSchema] = []
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CreatePackSchema(BaseSchema):
    name: str
    description: str | None = None
    tags: list[int] = []


class UpdatePackSchema(BaseSchema):
    name: str | None = None
    description: str | None = None
    tags: list[int] = []



