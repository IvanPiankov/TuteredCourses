import pytest

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    scoped_session,
    Session as SessionType
)

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text,
    Enum
)


from models import DB_URL, DB_ECHO, Base, User, query_all_users



@pytest.fixture(scope="session")
def connection():
    engine = create_engine(url=DB_URL, echo=DB_ECHO)
    return engine.connect()



@pytest.fixture(scope="session")
def setup_database(connection):
    Base.metadata.bind = connection
    Base.metadata.create_all()


    yield

    Base.metadata.drop_all()

# def seed_database():
#     user = User(first_name="first_name", last_name="last_name", abstract="abstract")
#     # users = [
#     #     {
#     #         "id": 1,
#     #         "name": "John Doe",
#     #     },
#     #     # ...
#     # ]
#
#     db_session.add(user)
#     db_session.commit()


@pytest.fixture
def db_session(connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()



def test_all_users(db_session):
    user = User(first_name="first_name", last_name="last_name", abstract="abstract")
    db_session.add(user)
    db_session.commit()
    actual_result = query_all_users(db_session)
    assert 1 == len(actual_result)