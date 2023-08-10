from typing import Any, Generator
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_signin(async_client: Generator[AsyncClient, Any, Any]):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Hello World!"
