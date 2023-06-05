import pytest
import pytest_asyncio
from db.config import get_session
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.dto.user_dto import UserDTO
from src.user.user_service import UserService
from src.user.user_repo import UserRepo
from tests.user.mock_user_repo import MockUserRepo


@pytest_asyncio.fixture(scope="module")
async def user_repo():
    return UserRepo(db=get_session)


@pytest_asyncio.fixture(scope="function")
async def add_user(user_repo: UserRepo, user: UserDTO):
    _ = user_repo.add_user(create_user=user)
    return user


@pytest_asyncio.fixture(scope="function")
async def activated_user(user_repo: UserRepo, add_user: UserDTO):
    user_repo.update_activation_flag(user=add_user, activated=True)
    add_user.activated = True
    return add_user


@pytest_asyncio.fixture(scope="function")
async def user():
    return CreateUserDTO(
        first_name="John",
        last_name="Doe",
        email="johndoe@gmail.com",
        password="Welcome1",
    )


@pytest.fixture()
def setup_user_service() -> UserService:
    user_service = UserService(user_repo=MockUserRepo())
    yield user_service
