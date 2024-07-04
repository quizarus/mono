import pytest

from app.quiz.models import Pack, Question
from app.quiz.si_importer.pack_loader import load
from app.quiz.tests.factories import QuestionFactory, TagFactory, PackFactory, AnswerFactory


@pytest.fixture
async def tag(async_session):
    tag = await TagFactory.create()
    await async_session.refresh(tag, attribute_names=['questions', 'packs'])
    yield tag


@pytest.fixture
async def pack(async_session, tag):
    pack = await PackFactory.create()
    await async_session.refresh(pack, attribute_names=['tags'])
    pack.tags.append(tag)
    await async_session.commit()
    yield pack


@pytest.fixture
async def question(async_session, tag):

    question = await QuestionFactory.create()
    await async_session.refresh(question, attribute_names=['tags'])
    question.tags.append(tag)
    await async_session.commit()
    yield question


@pytest.fixture
async def answer(async_session):

    answer = await AnswerFactory.create()
    yield answer
