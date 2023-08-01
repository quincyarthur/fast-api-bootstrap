from typing import Any, Generator
from httpx import AsyncClient
import pytest
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.dto.user_dto import UserDTO


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
