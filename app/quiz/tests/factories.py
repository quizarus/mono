import factory
import pytest
from factory import LazyFunction

from app.quiz.models import Pack, Question, Answer, Tag
from app.tests.factories.base import AsyncFactory
from faker import Faker

fake = Faker()


class PackFactory(AsyncFactory):
    class Meta:
        model = Pack

    name: str = LazyFunction(fake.name)


class QuestionFactory(AsyncFactory):
    class Meta:
        model = Question

    name: str = LazyFunction(fake.name)
    description: str = LazyFunction(fake.name)
    pack: int = factory.SubFactory(PackFactory)


class AnswerFactory(AsyncFactory):
    class Meta:
        model = Answer

    text: str = LazyFunction(fake.name)
    question: int = factory.SubFactory(QuestionFactory)


class TagFactory(AsyncFactory):
    class Meta:
        model = Tag

    name: str = LazyFunction(fake.name)