import pytest
import json
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.enum.user_origins import UserOrigins



@pytest.mark.asyncio
async def test_create_user(client):
    user = CreateUserDTO(
        first_name="john",
        last_name="doe",
        email="johndoe@gmail.com",
        origin=UserOrigins.LOCAL.value,
        password="secret",
    )
    response = client.post("/user/", json.dumps(user.__dict__))
    assert response.status_code == 200
    assert response.json()["first_name"] == user.first_name
    assert response.json()["last_name"] == user.last_name
    assert response.json()["email"] == user.email
    assert response.json()["origin"] == user.origin
    assert response.json()["activated"] == True
    assert response.json()["password"] is None
    assert response.json()["id"] is not None
