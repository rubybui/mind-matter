import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from mind_matter_api.models import db, User

@pytest.fixture(scope="session")
def db_engine():
    """
    Create a test database engine and bind it to SQLAlchemy.
    """
    engine = create_engine("sqlite:///./test.db")
    db.metadata.bind = engine
    db.metadata.create_all(bind=engine) 
    yield engine
    db.metadata.drop_all(bind=engine)  


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Provide a clean database session for each test function.
    """
    TestSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db_engine))
    db.session = TestSession
    print(f"DB URL: {db.metadata.bind}")
    yield db.session