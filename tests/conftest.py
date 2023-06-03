import pytest
import asyncio
import pytest_asyncio
from httpx import AsyncClient
from main import app
from tests.user.mock_user_repo import MockUserRepo
from src.user.user_service import UserService
from db.config import Base, get_session, engine, AsyncSession
from src.email.send_in_blue import SendInBlue
from tests.email.mock_email_service import MockEmailService
from typing import Any
from typing import Generator


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_client():
    app.dependency_overrides[SendInBlue] = MockEmailService
    async with AsyncClient(app=app, base_url=f"http://localhost:3000") as client:
        """
        Create a fresh database on each test case.
        """
        Base.metadata.create_all(engine)
        yield client
        Base.metadata.drop_all(engine)


@pytest.fixture()
def setup_user_service() -> UserService:
    user_service = UserService(user_repo=MockUserRepo())
    yield user_service
