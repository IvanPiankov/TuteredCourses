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

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    scoped_session,
    Session as SessionType
)


DB_URL = "sqlite:///homework-01.db"
DB_ECHO = True
engine = create_engine(url=DB_URL, echo=DB_ECHO)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(40), unique=True)
    last_name = Column(String(40), nullable=False)
    abstract = Column(Text)

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"first_name={self.first_name}, "
            f"last_name={self.last_name}, "
            f"abstract={self.abstract})"
        )

    def __repr__(self):
        return str(self)


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("user.id"))
    course_name = Column(String(80), unique=True)
    description = Column(Text)
    label = Column(String(50))

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"author_id={self.author_id}, "
            f"course_name={self.course_name}, "
            f"description={self.description},"
            f"label={self.label}"
        )

    def __repr__(self):
        return str(self)


def query_all_users(session: SessionType) -> [User]:
    users = session.query(User).all()
    return users


def query_user_by_first_name_and_last_name(session: SessionType, first_name: str,
                                           last_name: str) -> User:
    user = session.query(User).filter_by(first_name=first_name, last_name=last_name).one()
    return user


def query_all_courses(session: SessionType) -> [Course]:
    courses = session.query(Course).all()
    return courses


def query_all_courses_by_author_id(session: SessionType, author_id: str) -> [Course]:
    courses_one_user = session.query(User).filter_by(author_id=author_id).all()
    return courses_one_user


def create_user(session: SessionType, first_name: str, last_name: str, abstract: str) -> User:
    user = User(first_name=first_name, last_name=last_name, abstract=abstract)
    session.add(user)
    session.commit()
    return user


def create_course(session: SessionType, author_id: str, course_name: str, description: str, label: str) -> Course:
    course = Course(author_id=author_id, course_name=course_name, description=description, label=label)
    session.add(course)
    session.commit()
    return course


# def main():
#     # Base.metadata.create_all()
#     session: SessionType = Session()
#
#     # query_all_users(session)
#     query_user_by_first_name_and_last_name(session, "test", "test")
#     # create_user(session, "test", "test", "sttsts")
#     session.close()
#
#
# if __name__ == '__main__':
#     main()



