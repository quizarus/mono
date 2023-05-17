from app.dao import BaseEntityManager
from app.quiz.models import Answer


class AnswerEntityManager(BaseEntityManager):
    model = Answer
