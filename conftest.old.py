import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import create_async_engine

from app.database import SQLALCHEMY_DATABASE_URL, Base
from app.database import SessionLocal as Session

TEST_DB_NAME = "testdb"


@pytest.fixture(scope="session")
async def connection(request):
    # Modify this URL according to your database backend
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@localhost",
        echo=True
    )

    async with engine.connect() as connection:
        await connection.execute(f"CREATE DATABASE {TEST_DB_NAME} CHARACTER SET = 'utf8'")

    # Create a new engine/connection that will actually connect
    # to the test database we just created. This will be the
    # connection used by the test suite run.
    engine = create_engine(
        f"postgresql+asyncpg://postgres:postgres@localhost/{TEST_DB_NAME}"
    )
    connection = engine.connect()

    def teardown():
        connection.execute(f"DROP DATABASE {TEST_DB_NAME}")
        connection.close()

    request.addfinalizer(teardown)
    return connection


@pytest.fixture(scope="session", autouse=True)
def setup_db(connection, request):
    """Setup test database.

    Creates all database tables as declared in SQLAlchemy models,
    then proceeds to drop all the created tables after all tests
    have finished running.
    """
    Base.metadata.bind = connection
    Base.metadata.create_all(bind=connection)

    def teardown():
        Base.metadata.drop_all()

    request.addfinalizer(teardown)


@pytest.fixture(autouse=True)
def session(connection, request):
    transaction = connection.begin()
    session = Session(bind=connection)
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(db_session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    def teardown():
        Session.remove()
        transaction.rollback()

    request.addfinalizer(teardown)
    return session