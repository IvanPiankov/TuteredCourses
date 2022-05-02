import pytest

from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
)

from sqlalchemy import (
    create_engine,
)


from models import (
    DB_URL,
    DB_ECHO,
    Base,
    User,
    query_all_users,
    query_all_courses,
    Course,
    query_user_by_first_name_and_last_name,
    query_all_courses_by_author_id,
    create_user,
    create_course)



@pytest.fixture(scope="session")
def connection():
    engine = create_engine(url=DB_URL, echo=DB_ECHO)
    return engine.connect()


def seed_database(db_session):
    users = [
        {
            "first_name": "User_1",
            "last_name": "Userovich_1",
            "abstract": "abstract_1",
        },
        {
            "first_name": "User_2",
            "last_name": "Userovich_2",
            "abstract": "abstract_2",
        }
    ]
    for user in users:
        db_user = User(**user)
        db_session.add(db_user)
    courses = [
        {
            "author_id": 1,
            "course_name": "Course_1",
            "description": "Course_1_description",
            "label": "biology",
        },
        {
            "author_id": 1,
            "course_name": "Course_2",
            "description": "Course_2_description",
            "label": "math",
        }
    ]
    for course in courses:
        db_course = Course(**course)
        db_session.add(db_course)
    db_session.commit()


@pytest.fixture(scope="session")
def create_connection(connection):
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection))
    return Session


@pytest.fixture(scope="session")
def setup_database(connection, create_connection):
    Base.metadata.bind = connection
    Base.metadata.create_all()

    seed_database(create_connection)

    yield

    Base.metadata.drop_all()


@pytest.fixture
def db_session(setup_database, connection, create_connection):
    transaction = connection.begin()
    yield create_connection
    transaction.rollback()


def test_all_users(db_session):
    actual_result = query_all_users(db_session)
    assert 2 == len(actual_result)


def test_all_course(db_session):
    actual_result = query_all_courses(db_session)
    assert 2 == len(actual_result)


def test_query_by_name_and_last_name(db_session):
    actual_result = query_user_by_first_name_and_last_name(db_session, first_name="User_1", last_name="Userovich_1")
    assert "User_1" == actual_result.first_name


def test_query_course_by_id(db_session):
    actual_result = query_all_courses_by_author_id(db_session, author_id=1)
    assert 2 == len(actual_result)


def test_create_user(db_session):
    create_user(db_session, first_name="test", last_name="testtovich", abstract="test_abstract")
    actual_result = db_session.query(User).all()
    assert 3 == len(actual_result)


def test_create_course(db_session):
    create_course(db_session, author_id=1, label="test_1_test", course_name="test_11", description="test_abstract")
    actual_result = db_session.query(Course).all()
    assert 3 == len(actual_result)


def test_query_all(db_session):
    actual_result = db_session.query(Course).all()
    assert 2 == len(actual_result)

    actual_result = db_session.query(User).all()
    assert 2 == len(actual_result)


def test_query_user_by_name(db_session):
    actual_result = db_session.query(User).filter_by(first_name="User_1").one()
    assert 1 == actual_result.id


def test_query_course_by_name(db_session):
    actual_result = db_session.query(Course).filter_by(author_id=1).all()
    assert 2 == len(actual_result)
