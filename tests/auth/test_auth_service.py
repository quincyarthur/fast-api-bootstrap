from typing import Any, Generator
from fastapi import HTTPException
import pytest
import utils.jwt
from src.auth.auth_service import AuthService
from src.auth.enum.auth_exceptions import AuthExceptions


async def test_get_current_user_returns_token_expired_exception_if_no_token_expiration(
    monkeypatch: Generator[pytest.MonkeyPatch, Any, Any], anyio_backend
):
    def mock_return(*args, **kargs):
        return {"exp": None}

    with pytest.raises(HTTPException) as exc:
        monkeypatch.setattr(utils.jwt, "decode_token", mock_return)
        await AuthService().get_current_user(token="")
        assert str(exc.value) == AuthExceptions.TOKEN_EXPIRED.value


async def test_get_current_user_returns_invalid_token_exception_if_invalid_token(
    monkeypatch: Generator[pytest.MonkeyPatch, Any, Any], anyio_backend
):
    with pytest.raises(HTTPException) as exc:
        await AuthService().get_current_user(token="invalid token")
        assert str(exc.value) == AuthExceptions.INVALID_TOKEN.value
