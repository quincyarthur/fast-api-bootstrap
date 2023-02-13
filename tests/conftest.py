import pytest
from tests.user.mock_user_repo import MockUserRepo
from src.user.user_service import UserService


@pytest.fixture()
def setup_user_service() -> UserService:
    user_service = UserService(user_repo=MockUserRepo())
    yield user_service
