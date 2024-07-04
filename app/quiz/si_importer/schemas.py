from uuid import UUID

from fastapi import UploadFile, File
from pydantic import BaseModel, validator, Field


class PackUploadRequest(BaseModel):
    file: UploadFile = File(..., description="The file to upload")
    # Добавляем ограничение с помощью pydantic Field
    file_name: str = Field(..., regex=r"^.*\.siq$", description="The name of the file")


class PackUploadResponse(BaseModel):
    message: str


class QuestionSchema(BaseModel):
    uuid: UUID
    cost: int
    type: str
    text: str
    answer: str
    content: str | None = None
    attachments: dict[str, str | None] = {}


class ThemeSchema(BaseModel):
    name: str
    questions: list[QuestionSchema]


class RoundSchema(BaseModel):
    name: str
    themes: list[ThemeSchema]


class PackSchema(BaseModel):
    name: str
    rounds: list[RoundSchema]
    description: str = ''
