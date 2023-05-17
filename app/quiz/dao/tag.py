from app.dao import BaseEntityManager
from app.quiz.models import Tag


class TagEntityManager(BaseEntityManager):
    model = Tag
