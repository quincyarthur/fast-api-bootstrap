import pytest
from src.user.dto.user_dto import UserDTO
import json


@pytest.mark.asyncio
async def test_signin(async_client, activated_user: UserDTO):
    response = await async_client.post(
        "/auth/signin/",
        data={"username": activated_user.email, "password": activated_user.password},
    )
    assert response.status_code == 200
    assert type(response.json().get("access_token")) is str
    assert response.json().get("token_type") == "bearer"
