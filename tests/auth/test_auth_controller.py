import pytest
from src.user.enum.user_origins import UserOrigins


@pytest.mark.asyncio
async def test_signin(async_client, activated_user):
    response = await async_client.post("/user/", json=user.__dict__)
    assert response.status_code == 200
    assert response.json()["first_name"] == user.first_name
    assert response.json()["last_name"] == user.last_name
    assert response.json()["email"] == user.email
    assert response.json()["origin"] == UserOrigins.LOCAL.value
    assert response.json()["activated"] == False
    assert response.json()["password"] is None
    assert response.json()["id"] is not None
