from tests.user.mock_user_repo import MockUserRepo
from src.user.user_service import UserService
import pytest
from src.user.dto.user_dto import UserDTO
from fastapi import HTTPException
from src.user.enum.user_exceptions import UserExceptions
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.enum.user_origins import UserOrigins


@pytest.fixture()
def setup() -> UserService:
    user_service = UserService(user_repo=MockUserRepo())
    yield user_service


@pytest.mark.anyio
async def test_find_by_id_returns_UserDTO_if_found(setup: UserService):
    user = await setup.find_by_id(id=1)
    assert type(user) is UserDTO


@pytest.mark.anyio
async def test_find_by_id_returns_exception_if_not_found(setup: UserService):
    with pytest.raises(HTTPException) as exc:
        await setup.find_by_id(id=2)
        assert str(exc.value) == UserExceptions.ID_NOT_FOUND.value


@pytest.mark.anyio
async def test_find_by_email_returns_UserDTO_if_found(setup: UserService):
    user = await setup.find_by_email(email="johndoe@gmail.com")
    assert type(user) is UserDTO


@pytest.mark.anyio
async def test_find_by_email_returns_exception_if_not_found(setup: UserService):
    with pytest.raises(HTTPException) as exc:
        await setup.find_by_email(email="unknown@gmail.com")
        assert str(exc.value) == UserExceptions.EMAIL_NOT_FOUND.value


@pytest.mark.anyio
async def test_add_user_returns_exception_if_email_exists(setup: UserService):
    create_user = CreateUserDTO(
        first_name="John",
        last_name="Doe",
        email="johndoe@gmail.com",
        password="Welcome",
        origin=UserOrigins.LOCAL.value,
    )
    with pytest.raises(HTTPException) as exc:
        await setup.add_user(create_user=create_user)
        assert str(exc.value) == UserExceptions.EMAIL_EXISTS.value


@pytest.mark.anyio
async def test_exclude_password_returns_null_password(setup: UserService):
    user = UserDTO(
        first_name="John",
        last_name="Doe",
        email="johndoe@gmail.com",
        origin=UserOrigins.LOCAL.value,
        activated=False,
        password="secret",
        id=1,
    )
    assert user.password is not None
    user = await setup.exclude_password(user=user)
    assert user.password is None


@pytest.mark.anyio
async def test_validate_email_returns_str_if_valid_email(setup: UserService):
    email = "johndoe@gmail.com"
    email = setup.valiate_email(email=email, check_deliverability=True)
    assert type(email) is str


@pytest.mark.anyio
async def test_validate_email_throws_exception_if_not_valid_email(setup: UserService):
    email = "johndoe@dfdsffafsafd.moc"
    with pytest.raises(HTTPException) as exc:
        validated_email = setup.valiate_email(email=email, check_deliverability=True)
