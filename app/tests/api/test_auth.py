import pytest
from httpx import AsyncClient

from app.core.config import settings

pytestmark = pytest.mark.asyncio


async def test_jwt_login(client: AsyncClient) -> None:
    response = await client.post(
        "/auth/jwt/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD
        }
    )
    data = response.json()
    assert data['access_token'] != ""
    assert data['token_type'] == "bearer"
