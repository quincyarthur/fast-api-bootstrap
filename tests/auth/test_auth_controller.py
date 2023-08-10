from typing import Any, Generator
from httpx import AsyncClient
import pytest
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.dto.user_dto import UserDTO
from fastapi import HTTPException
from src.auth.enum.auth_exceptions import AuthExceptions
from src.user.enum.user_exceptions import UserExceptions
from src.auth.config import oauth


@pytest.mark.asyncio
async def test_signin(
    async_client: Generator[AsyncClient, Any, Any],
    activated_user: UserDTO,
    user: CreateUserDTO,
):
    data = {"username": activated_user.email, "password": user.password}
    response = await async_client.post(
        "/auth/signin",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert type(response.json().get("access_token")) is str
    assert response.json().get("token_type") == "bearer"


@pytest.mark.asyncio
async def test_signin_throws_not_activated_exception(
    async_client: Generator[AsyncClient, Any, Any],
    add_user: UserDTO,
    user: CreateUserDTO,
):
    data = {"username": add_user.email, "password": user.password}
    response = await async_client.post(
        "/auth/signin",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400
    assert response.json().get("detail") == AuthExceptions.NOT_ACTIVATED.value


@pytest.mark.asyncio
async def test_signin_throws_wrong_password_exception(
    async_client: Generator[AsyncClient, Any, Any], activated_user: UserDTO
):
    data = {"username": activated_user.email, "password": "wrong_password"}
    response = await async_client.post(
        "/auth/signin",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400
    assert response.json().get("detail") == AuthExceptions.WRONG_PASSWORD.value


@pytest.mark.asyncio
async def test_signin_throws_email_not_found_exception(
    async_client: Generator[AsyncClient, Any, Any],
    user: CreateUserDTO,
):
    data = {"username": "wrong_email", "password": user.password}
    response = await async_client.post(
        "/auth/signin",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400
    assert response.json().get("detail") == UserExceptions.EMAIL_NOT_FOUND.value


@pytest.mark.asyncio
async def test_google_auth_creates_user_and_generates_token_when_email_not_found_exception(
    async_client: Generator[AsyncClient, Any, Any],
    user: CreateUserDTO,
    monkeypatch: Generator[pytest.MonkeyPatch, Any, Any],
):
    async def mockreturn(*args, **kargs):
        return {
            "userinfo": {
                "email": user.email,
                "given_name": user.first_name,
                "family_name": user.last_name,
            }
        }

    monkeypatch.setattr(oauth.google, "authorize_access_token", mockreturn)
    response = await async_client.get("/auth/google")
    assert response.status_code == 200
    assert response.json().get("token_type") == "bearer"
    assert type(response.json().get("access_token")) is str
