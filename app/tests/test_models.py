import logging

import pytest
from sqlalchemy import select, func, update
from sqlalchemy.orm import selectinload, joinedload

from app.quiz.models import Pack, Question, Answer, Tag
from app.quiz.tests.factories import PackFactory, QuestionFactory, AnswerFactory

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


class TestPack:

    @pytest.mark.skip
    async def test_1(self, async_session):
        obj = MyModel(name='first')
        obj2 = MyModel(name='second')
        s = async_session.add(obj)
        async_session.add(obj2)
        b = await async_session.commit()

        created_obj = await async_session.get(MyModel, obj.id)
        result = await async_session.execute(select(MyModel))
        objects = result.scalars().all()
        assert True

    async def test_m2m_pack_and_tag(self, async_session):

        pack = Pack(name='first pack')
        tag = Tag(name='my tag')

        pack.tags.append(tag)

        async_session.add(pack)
        async_session.add(tag)
        await async_session.commit()

        result = await async_session.execute(select(Pack).options(joinedload(Pack.tags)))
        created_pack = result.unique().scalars().first()
        assert tag in created_pack.tags
        assert created_pack in tag.packs

    async def test_m2m_question_and_tag(self, async_session, question, tag):
        # result = await async_session.execute(select(Question).where(Question.id == question.id).options(selectinload(Question.tags)))
        # question = result.unique().scalars().first()
        question.tags.append(tag)
        await async_session.commit()
        assert tag in question.tags

    async def test_pack_factory(self, async_session, pack):
        # await PackFactory.create()
        count = await async_session.scalar(
            select(func.count()).select_from(Pack)
        )
        assert count == 1

    async def test_question_factory(self, async_session):
        q = await QuestionFactory.create()
        query = select(Question).options(selectinload(Question.pack))
        result = await async_session.execute(query)
        question = result.scalars().first()
        assert question.pack.name == q.pack.name

    async def test_answer_factory(self, async_session, answer):
        query = select(Answer).options(
            selectinload(Answer.question).selectinload(Question.pack)
        )
        result = await async_session.execute(query)
        a = result.scalars().first()
        assert a.question.name == answer.question.name
        assert a.question.pack.name == answer.question.pack.name

    async def test_batch(self, async_session):
        packs = [Pack(name='pack 1'), Pack(name='pack 2')]
        async_session.add_all(packs)
        await async_session.commit()

        to_update = [
            {'id': 1, 'name': 'new name'},
            {'id': 2, 'name': 'new name'}
        ]

        await async_session.execute(
            update(Pack),
            to_update
        )
        await async_session.commit()


        result = await async_session.execute(select(Pack))
        created_packs = result.unique().scalars().all()

        for p, pack in zip(to_update, created_packs):
            assert p['name'] == pack.name
