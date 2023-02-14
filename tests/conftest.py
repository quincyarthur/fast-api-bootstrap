import pytest
from tests.user.mock_user_repo import MockUserRepo
from src.user.user_service import UserService
from typing import Any
from typing import Generator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.config import Base, get_session
from src.user import user_controller
from src.auth import auth_controller
from src.email.send_in_blue import SendInBlue
from tests.email.mock_email_service import MockEmailService

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def start_application():
    app = FastAPI()
    app.include_router(user_controller.router)
    app.include_router(auth_controller.router)
    return app


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session] = _get_test_db
    app.dependency_overrides[SendInBlue] = MockEmailService
    with TestClient(app) as client:
        yield client


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def setup_user_service() -> UserService:
    user_service = UserService(user_repo=MockUserRepo())
    yield user_service
