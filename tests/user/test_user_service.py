from tests.user.mock_user_repo import MockUserRepo
from src.user.user_service import UserService
import pytest
from src.user.dto.user_dto import UserDTO


@pytest.mark.anyio
async def test_find_by_id_returns_UserDTO():
    user_service = UserService(user_repo=MockUserRepo())
    user = await user_service.find_by_id(id=1)
    assert type(user) is UserDTO
