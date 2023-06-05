import pytest
import pytest_asyncio
from src.user.dto.user_dto import UserDTO


@pytest_asyncio.fixture(scope="function")
async def jwt(async_client, activated_user: UserDTO) -> str:
    data = {"username": activated_user.email, "password": activated_user.password}
    response = await async_client.post("/signin/", data=data)
    return response.json().get("access_token")
