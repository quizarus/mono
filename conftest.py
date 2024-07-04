import asyncio
import json

import pytest
import pytest_asyncio
from httpx import AsyncClient
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import text

from app.config import settings
from app.database import get_engine, get_db, SQLALCHEMY_DATABASE_URI
from app.quiz.models import *
from main import app as fast_api_app

fixtures = [
    'app.quiz.tests.fixtures',
    'app.quiz.si_importer.tests.fixtures'
]

pytest_plugins = fixtures


# TEST_DB_URI = 'postgresql+asyncpg://postgres:postgres@localhost/test_db'

@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def override_get_db():
    return AsyncTestSessionManager(SQLALCHEMY_DATABASE_URI).session


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

    session_manager = AsyncTestSessionManager(SQLALCHEMY_DATABASE_URI)
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


@pytest.fixture
def minio_client():
    client = Minio(settings.S3_HOST, access_key=settings.S3_ACCESS_KEY, secret_key=settings.S3_SECRET_KEY,
                   secure=settings.S3_SECURE)
    if not client.bucket_exists(settings.S3_BUCKET):
        client.make_bucket(settings.S3_BUCKET)
    if not client.bucket_exists(settings.S3_PUBLIC_BUCKET):
        client.make_bucket(settings.S3_PUBLIC_BUCKET)
        policy = {
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": [
                            "*"
                        ]
                    },
                    "Action": [
                        "s3:GetBucketLocation",
                        "s3:ListBucket"
                    ],
                    "Resource": [
                        f"arn:aws:s3:::{settings.S3_PUBLIC_BUCKET}"
                    ]
                },
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": [
                            "*"
                        ]
                    },
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Resource": [
                        f"arn:aws:s3:::{settings.S3_PUBLIC_BUCKET}/*"
                    ]
                }
            ],
            "Version": "2012-10-17"
        }
        client.set_bucket_policy(settings.S3_PUBLIC_BUCKET, json.dumps(policy))
    yield client
    for bucket in (settings.S3_BUCKET, settings.S3_PUBLIC_BUCKET):
        objects = client.list_objects(bucket, recursive=True)
        for obj in objects:
            client.remove_object(bucket, obj.object_name)
        client.remove_bucket(bucket)
