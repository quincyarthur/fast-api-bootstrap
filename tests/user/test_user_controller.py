import pytest
from src.user.enum.user_origins import UserOrigins


@pytest.mark.asyncio
async def test_create_user(async_client, user):
    response = await async_client.post("/user/", json=user.__dict__)
    assert response.status_code == 200
    assert response.json().get("first_name") == user.first_name
    assert response.json().get("last_name") == user.last_name
    assert response.json().get("email") == user.email
    assert response.json().get("origin") == UserOrigins.LOCAL.value
    assert response.json().get("activated") == False
    assert response.json().get("password") is None
    assert response.json().get("id") is not None


# @pytest.mark.asyncio
# async def test_get_current_user(async_client, add_user):
#     response = await async_client.post("/user/", json=add_user)
