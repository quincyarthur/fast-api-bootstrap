import pytest
from src.user.user_service import UserService
from src.user.dto.user_dto import UserDTO
from fastapi import HTTPException
from src.user.enum.user_exceptions import UserExceptions
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.enum.user_origins import UserOrigins


async def test_find_by_id_returns_UserDTO_if_found(
    setup_user_service: UserService, anyio_backend
):
    user = await setup_user_service.find_by_id(id=1)
    assert type(user) is UserDTO


async def test_find_by_id_returns_exception_if_not_found(
    setup_user_service: UserService, anyio_backend
):
    with pytest.raises(HTTPException) as exc:
        await setup_user_service.find_by_id(id=2)
        assert str(exc.value) == UserExceptions.ID_NOT_FOUND.value


async def test_find_by_email_returns_UserDTO_if_found(
    setup_user_service: UserService, anyio_backend
):
    user = await setup_user_service.find_by_email(email="johndoe@gmail.com")
    assert type(user) is UserDTO


async def test_find_by_email_returns_exception_if_not_found(
    setup_user_service: UserService, anyio_backend
):
    with pytest.raises(HTTPException) as exc:
        await setup_user_service.find_by_email(email="unknown@gmail.com")
        assert str(exc.value) == UserExceptions.EMAIL_NOT_FOUND.value


async def test_add_user_returns_exception_if_email_exists(
    setup_user_service: UserService, anyio_backend
):
    create_user = CreateUserDTO(
        first_name="John",
        last_name="Doe",
        email="johndoe@gmail.com",
        password="Welcome",
        origin=UserOrigins.LOCAL.value,
    )
    with pytest.raises(HTTPException) as exc:
        await setup_user_service.add_user(create_user=create_user)
        assert str(exc.value) == UserExceptions.EMAIL_EXISTS.value


async def test_exclude_password_returns_null_password(
    setup_user_service: UserService, anyio_backend
):
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
    user = await setup_user_service.exclude_password(user=user)
    assert user.password is None


async def test_validate_email_returns_str_if_valid_email(
    setup_user_service: UserService, anyio_backend
):
    email = "johndoe@gmail.com"
    email = setup_user_service.valiate_email(email=email, check_deliverability=True)
    assert type(email) is str


async def test_validate_email_throws_exception_if_not_valid_email(
    setup_user_service: UserService, anyio_backend
):
    email = "johndoe@dfdsffafsafd.moc"
    with pytest.raises(HTTPException) as exc:
        validated_email = setup_user_service.valiate_email(
            email=email, check_deliverability=True
        )
