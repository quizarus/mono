import uuid

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models import Base, BaseModel

pack_and_tag_association = Table(
    "question_pack__tag__association",
    Base.metadata,
    Column("pack_id", ForeignKey("question_pack.id"), primary_key=True),
    Column("tag_id", ForeignKey("question_tag.id"), primary_key=True),
)

question_and_tag_association = Table(
    "question__tag__association",
    Base.metadata,
    Column("question_id", ForeignKey("question.id"), primary_key=True),
    Column("tag_id", ForeignKey("question_tag.id"), primary_key=True),
)


class Pack(BaseModel):
    __tablename__ = 'question_pack'

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text())
    icon: Mapped[str | None] = mapped_column(String(255))
    questions: Mapped[list['Question']] = relationship("Question", back_populates='pack')

    tags: Mapped[list["Tag"]] = relationship(secondary=pack_and_tag_association, back_populates="packs", lazy='joined')

    def __str__(self):
        return self.name


class Question(BaseModel):
    __tablename__ = 'question'

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text())
    pack_id: Mapped[int] = mapped_column(Integer, ForeignKey('question_pack.id', ondelete="CASCADE"))
    pack: Mapped[Pack] = relationship(back_populates='questions', lazy="joined")

    answers: Mapped[list['Answer']] = relationship("Answer", back_populates='question')
    tags: Mapped[list["Tag"]] = relationship(secondary=question_and_tag_association, back_populates="questions", lazy="joined")


#
class Answer(BaseModel):
    __tablename__ = 'question_answer'

    is_right: Mapped[bool] = mapped_column(default=False)
    text: Mapped[str] = mapped_column(String(255))
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey('question.id', ondelete="CASCADE"))
    question: Mapped[Question] = relationship(back_populates='answers')


class Tag(BaseModel):
    __tablename__ = 'question_tag'

    name: Mapped[str] = mapped_column(String(255))
    packs: Mapped[list["Pack"]] = relationship(secondary=pack_and_tag_association, back_populates="tags")
    questions: Mapped[list["Question"]] = relationship(secondary=question_and_tag_association, back_populates="tags")
