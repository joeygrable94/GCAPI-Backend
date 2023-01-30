from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.utils import random_email, random_lower_string

from app.api.errors import ErrorCode
from app.core.config import settings

pytestmark = pytest.mark.asyncio


async def test_create_user_as_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    data: Dict[str, str] = {"email": username, "password": password}
    response: Response = await client.post(
        "users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    a_user: Dict[str, Any] = response.json()
    assert "id" in a_user
    assert a_user["email"] == username
    assert "hashed_password" not in a_user
    assert "password" not in a_user
    assert a_user["is_active"]
    assert not a_user["is_verified"]
    assert not a_user["is_superuser"]


async def test_create_user_as_superuser_user_already_exists(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    password: str = random_lower_string()
    data: Dict[str, str] = {"email": settings.TEST_NORMAL_USER, "password": password}
    response: Response = await client.post(
        "users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    a_user: Dict[str, Any] = response.json()
    assert a_user["detail"] == ErrorCode.USER_ALREADY_EXISTS


async def test_create_user_as_superuser_password_too_long(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    username: str = random_email()
    password: str = random_lower_string() * 10
    data: Dict[str, str] = {"email": username, "password": password}
    response: Response = await client.post(
        "users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    a_user: Dict[str, Any] = response.json()
    assert a_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
    assert (
        a_user["detail"]["reason"]
        == f"Password must contain {settings.PASSWORD_LENGTH_MAX} or less characters"
    )


async def test_create_user_as_superuser_password_too_short(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    username: str = random_email()
    password: str = "1234567"
    data: Dict[str, str] = {"email": username, "password": password}
    response: Response = await client.post(
        "users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    a_user: Dict[str, Any] = response.json()
    assert a_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
    assert (
        a_user["detail"]["reason"]
        == f"Password must contain {settings.PASSWORD_LENGTH_MIN} or more characters"
    )
