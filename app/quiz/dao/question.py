from app.dao import BaseEntityManager
from app.quiz.models import Question


class QuestionEntityManager(BaseEntityManager):
    model = Question
