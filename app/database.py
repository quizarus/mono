# from sqlalchemy import create_engine
import contextlib

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine

SQLALCHEMY_DATABASE_URI = \
    f"postgresql+asyncpg://" \
    f"{settings.POSTGRES_USER}" \
    f":{settings.POSTGRES_PASSWORD}" \
    f"@{settings.POSTGRES_HOSTNAME}" \
    f":{settings.DATABASE_PORT}" \
    f"/{settings.POSTGRES_DB}"


def get_engine(db_uri: str, debug: bool = False) -> AsyncEngine:
    return create_async_engine(
        db_uri,
        echo=debug,
    )


engine = get_engine(SQLALCHEMY_DATABASE_URI, debug=True)
session = async_sessionmaker(engine, expire_on_commit=False)


# @contextlib.asynccontextmanager
async def get_db():
    db = session()
    try:
        yield db
    finally:
        await db.close()
