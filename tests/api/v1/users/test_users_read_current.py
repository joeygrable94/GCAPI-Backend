from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response

from app.core.config import settings

pytestmark = pytest.mark.asyncio


async def test_read_current_superuser(
    client: AsyncClient, superuser_token_headers: Dict[str, str]
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    a_user: Dict[str, Any] = response.json()
    assert "id" in a_user
    assert a_user["email"] == settings.FIRST_SUPERUSER
    assert "hashed_password" not in a_user
    assert "password" not in a_user
    assert a_user["is_active"]
    assert a_user["is_verified"]
    assert a_user["is_superuser"]


async def test_read_current_testuser(
    client: AsyncClient, testuser_token_headers: Dict[str, str]
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=testuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    a_user: Dict[str, Any] = response.json()
    assert "id" in a_user
    assert a_user["email"] == settings.TEST_NORMAL_USER
    assert "hashed_password" not in a_user
    assert "password" not in a_user
    assert a_user["is_active"]
    assert a_user["is_verified"]
    assert not a_user["is_superuser"]
