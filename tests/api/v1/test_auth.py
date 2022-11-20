from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response

from app.api.errors import ErrorCode
from app.core.config import settings
from app.db.schemas import UserCreate, UserRead
from app.security import AuthManager
from tests.utils.utils import random_email, random_lower_string

pytestmark = pytest.mark.anyio


async def test_register_random_user(client: AsyncClient) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    data: Dict[str, str] = {"email": username, "password": password}
    response: Response = await client.post(
        "auth/register",
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


async def test_register_user_already_exists(client: AsyncClient) -> None:
    password: str = random_lower_string()
    data: Dict[str, str] = {"email": settings.TEST_NORMAL_USER, "password": password}
    response: Response = await client.post(
        "auth/register",
        json=data,
    )
    assert response.status_code == 400
    a_user: Dict[str, Any] = response.json()
    assert a_user["detail"] == ErrorCode.USER_ALREADY_EXISTS


async def test_auth_login_superuser(client: AsyncClient) -> None:
    r: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        },
    )
    tokens: Dict[str, Any] = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert "access_token_csrf" in tokens
    assert "refresh_token" in tokens
    assert "refresh_token_csrf" in tokens


async def test_auth_login_testuser(client: AsyncClient) -> None:
    r: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": settings.TEST_NORMAL_USER,
            "password": settings.TEST_NORMAL_USER_PASSWORD,
        },
    )
    tokens: Dict[str, Any] = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert "access_token_csrf" in tokens
    assert "refresh_token" in tokens
    assert "refresh_token_csrf" in tokens


async def test_auth_login_user_not_found(client: AsyncClient) -> None:
    not_username: str = random_email()
    password: str = random_lower_string()
    r: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": not_username,
            "password": password,
        },
    )
    data: Dict[str, Any] = r.json()
    assert r.status_code >= 400
    assert "detail" in data
    assert data.get("detail") == ErrorCode.BAD_CREDENTIALS


async def test_auth_login_user_not_verified(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    settings.USERS_REQUIRE_VERIFICATION = True
    email: str = random_email()
    password: str = random_lower_string()
    a_user: UserRead = await user_auth.users.create(
        schema=UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=False,
            is_verified=False,
        )
    )
    r: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": a_user.email,
            "password": password,
        },
    )
    assert r.status_code >= 400
    data: Dict[str, Any] = r.json()
    assert "detail" in data
    assert data["detail"] == ErrorCode.USER_NOT_VERIFIED


async def test_auth_logout_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    r: Response = await client.delete("auth/logout", headers=superuser_token_headers)
    data: Dict[str, str] = r.json()
    assert r.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] == ""
    assert data["access_token_csrf"] == ""
    assert data["refresh_token"] == ""
    assert data["refresh_token_csrf"] == ""


async def test_auth_logout_testuser(
    client: AsyncClient, testuser_token_headers: Dict[str, str]
) -> None:
    r: Response = await client.delete("auth/logout", headers=testuser_token_headers)
    data: Dict[str, str] = r.json()
    assert r.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] == ""
    assert data["access_token_csrf"] == ""
    assert data["refresh_token"] == ""
    assert data["refresh_token_csrf"] == ""