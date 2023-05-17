from app.dao import BaseEntityManager
from app.quiz.models import Pack


class PackEntityManager(BaseEntityManager):
    model = Pack


