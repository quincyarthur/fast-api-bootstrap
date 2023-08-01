from typing import Any, Generator
from httpx import AsyncClient
import pytest
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.dto.user_dto import UserDTO
import json


@pytest.mark.asyncio
async def test_signin(
    async_client: Generator[AsyncClient, Any, Any],
    activated_user: UserDTO,
    user: CreateUserDTO,
):
    response = await async_client.post(
        "/auth/signin",
        data={"username": "johndoe@gmail.com", "password": "Welcome1"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    print(f"Request: {response.request.__dict__}")
    print(f"Response: {response.__dict__}")
    assert response.status_code == 200
    assert type(response.json().get("access_token")) is str
    assert response.json().get("token_type") == "bearer"


# @pytest.mark.asyncio
# async def test_me(async_client: Generator[AsyncClient, Any, Any], jwt: str):
#     print(f"JWT: {jwt}")
#     response = await async_client.post(
#         "/users/me",
#         headers={"Authorization": f"Bearer {jwt}"},
#     )
#     print(f"Request: {response.request.__dict__}")
#     print(f"Response: {response.json()}")
#     assert response.status_code == 200
#     assert type(response.json().get("access_token")) is str
#     assert response.json().get("token_type") == "bearer"
