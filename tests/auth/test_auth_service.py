from typing import Any, Generator
from fastapi import HTTPException
import pytest
from src.user.dto.user_dto import UserDTO
import utils.jwt
from src.auth.auth_service import AuthService
from src.auth.enum.auth_exceptions import AuthExceptions
from src.user.user_service import UserService
from utils.password import Password


async def test_get_current_user_returns_token_expired_exception_if_no_token_expiration(
    monkeypatch: Generator[pytest.MonkeyPatch, Any, Any], anyio_backend
):
    def mock_return(*args, **kargs):
        return {"exp": None}

    with pytest.raises(HTTPException) as exc:
        monkeypatch.setattr(utils.jwt, "decode_token", mock_return)
        await AuthService().get_current_user(token="")
    assert str(exc.value.detail) == AuthExceptions.TOKEN_EXPIRED.value


async def test_get_current_user_returns_invalid_token_exception_if_invalid_token(
    anyio_backend,
):
    with pytest.raises(HTTPException) as exc:
        await AuthService().get_current_user(token="invalid token")
    assert str(exc.value.detail) == AuthExceptions.INVALID_TOKEN.value


async def test_signin_returns_not_activated_exception_if_user_not_activated(
    monkeypatch: Generator[pytest.MonkeyPatch, Any, Any],
    anyio_backend,
    setup_user_service: UserService,
    test_user: UserDTO,
):
    async def mock_return(*args, **kargs):
        return test_user

    with pytest.raises(HTTPException) as exc:
        monkeypatch.setattr(setup_user_service, "find_by_email", mock_return)
        await AuthService(user_service=setup_user_service).signin(
            email=test_user.email, password=test_user.password
        )
    assert str(exc.value.detail) == AuthExceptions.NOT_ACTIVATED.value


async def test_signin_returns_wrong_password_exception(
    monkeypatch: Generator[pytest.MonkeyPatch, Any, Any],
    anyio_backend,
    setup_user_service: UserService,
    test_user: UserDTO,
):
    pwd = Password()

    async def mock_return(*args, **kargs):
        test_user.activated = True
        test_user.password = pwd.hash("password")
        return test_user

    with pytest.raises(HTTPException) as exc:
        monkeypatch.setattr(setup_user_service, "find_by_email", mock_return)
        await AuthService(user_service=setup_user_service, pwd=pwd).signin(
            email=test_user.email, password="wrong_password"
        )
    assert str(exc.value.detail) == AuthExceptions.WRONG_PASSWORD.value
