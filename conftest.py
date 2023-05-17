import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import text

from app.database import get_engine, TEST_DB_URI, get_db
from app.quiz.models import *
from main import app as fast_api_app

fixtures = [
    'app.quiz.tests.fixtures'
]

pytest_plugins = fixtures

@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def override_get_db():
    return AsyncTestSessionManager(TEST_DB_URI).session


@pytest.fixture
def app():
    fast_api_app.dependency_overrides[get_db] = override_get_db
    return fast_api_app

@pytest_asyncio.fixture
async def async_client(app):
    async with AsyncClient(
            app=app,
            base_url=f"http://127.0.0.1:8000/api",
            follow_redirects=True
    ) as client:
        yield client


class AsyncTestSessionManager:
    """Keeps the same session for factories and requests via async_session"""

    obj = None

    def __new__(cls, db_uri: str, *args, **kwargs):
        if not cls.obj:
            obj = super().__new__(cls)
            engine = get_engine(db_uri, debug=True)
            session = async_sessionmaker(engine, expire_on_commit=False, future=True)()
            obj.engine = engine
            obj.session = session
            cls.obj = obj
        return cls.obj


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_session() -> AsyncSession:

    async def make_query(engine: AsyncEngine, queries: tuple):
        async with engine.connect() as connection:
            await connection.execution_options(isolation_level="AUTOCOMMIT")
            for query in queries:
                await connection.execute(text(query))

    session_manager = AsyncTestSessionManager(TEST_DB_URI)
    session = session_manager.session
    # await make_query(engine, (f"DROP DATABASE IF EXISTS {test_db_name}", f"CREATE DATABASE {test_db_name}"))
    async with session_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # session = AsyncSessionMaker()
    yield session

    await session.close()
    async with session_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # await make_query(engine, (f"DROP DATABASE {test_db_name}",))
