import pytest
from src.user.enum.user_origins import UserOrigins


@pytest.mark.asyncio
async def test_signin(async_client, activated_user):
    data = {"username": activated_user.email, "password": activated_user.password}
    response = await async_client.post("/auth/signin/", data=data)
    assert response.status_code == 200
    assert type(response.json()["access_token"]) is str
    assert response.json().get("token_type") == "bearer"
