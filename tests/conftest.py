from dotenv import load_dotenv
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
import json
from db.config import (
    async_session,
    get_session,
    create_async_engine,
    modules,
    TEST_DATABASE_URL,
    sessionmaker,
    AsyncSession,
)
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.dto.user_dto import UserDTO
from src.user.user_service import UserService
from src.user.user_repo import UserRepo
from src.user.enum.user_origins import UserOrigins
from tests.user.mock_user_repo import MockUserRepo

test_engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)

test_async_session = sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def override_db():
    try:
        print(f"Test: {test_engine.url}")
        db = test_async_session()
        yield db
    finally:
        await db.close()


@pytest_asyncio.fixture(scope="function")
async def async_client() -> Generator[AsyncClient, Any, Any]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        app.dependency_overrides[SendInBlue] = MockEmailService
        app.dependency_overrides[get_session] = override_db
        """
        Create a fresh database on each test case.
        """
        async with test_engine.begin() as conn:
            print("creating db...")
            await conn.run_sync(Base.metadata.create_all)

        yield client

        async with test_engine.begin() as conn:
            print("dropping db...")
            await conn.run_sync(Base.metadata.drop_all)


"""
User Fixtures
"""


@pytest_asyncio.fixture(scope="module")
async def user_repo():
    async with test_async_session() as session:
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
async def jwt(async_client, activated_user: UserDTO, user: CreateUserDTO) -> str:
    data = {"username": activated_user.email, "password": user.password}
    response = await async_client.post(
        "/auth/signin",
        data=json.dumps(data),
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    print(f"Response: {response}")
    return response.json().get("access_token")
