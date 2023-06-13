import pytest
import asyncio
import pytest_asyncio
from httpx import AsyncClient
from main import app
from db.config import Base, engine
from src.email.send_in_blue import SendInBlue
from tests.email.mock_email_service import MockEmailService
from typing import Any
from typing import Generator

from db.config import async_session
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.dto.user_dto import UserDTO
from src.user.user_service import UserService
from src.user.user_repo import UserRepo
from src.user.enum.user_origins import UserOrigins
from tests.user.mock_user_repo import MockUserRepo


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_client() -> Generator[AsyncClient, Any, Any]:
    app.dependency_overrides[SendInBlue] = MockEmailService
    async with AsyncClient(app=app, base_url=f"http://localhost:3000") as client:
        """
        Create a fresh database on each test case.
        """
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield client

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


"""
User Fixtures
"""


@pytest_asyncio.fixture(scope="module")
async def user_repo():
    async with async_session() as session:
        yield UserRepo(db=session)


@pytest_asyncio.fixture(scope="function")
async def add_user(user_repo: UserRepo, user: UserDTO) -> UserDTO:
    return await user_repo.add_user(create_user=user)


@pytest_asyncio.fixture(scope="function")
async def activated_user(user_repo: UserRepo, add_user: UserDTO) -> UserDTO:
    await user_repo.update_activation_flag(user=add_user, activated=True)
    add_user.activated = True
    return add_user


@pytest_asyncio.fixture(scope="function")
async def user():
    return CreateUserDTO(
        first_name="John",
        last_name="Doe",
        email="johndoe@gmail.com",
        password="Welcome1",
        origin=UserOrigins.LOCAL.value,
    )


@pytest.fixture()
def setup_user_service() -> UserService:
    user_service = UserService(user_repo=MockUserRepo())
    yield user_service


"""
Auth Fixtures
"""


@pytest_asyncio.fixture(scope="function")
async def jwt(async_client, activated_user: UserDTO) -> str:
    data = {"username": activated_user.email, "password": activated_user.password}
    response = await async_client.post("/auth/signin/", data=data)
    return response.json().get("access_token")
