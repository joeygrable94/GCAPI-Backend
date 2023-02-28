from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.users import create_new_user
from tests.utils.utils import random_email, random_lower_string

from app.api.errors import ErrorCode
from app.core.config import settings
from app.db.schemas import UserCreate
from app.db.schemas.user import UserPrincipals
from app.db.tables.user import User
from app.security import AuthManager

pytestmark = pytest.mark.asyncio


async def test_auth_login_superuser(client: AsyncClient) -> None:
    response: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        },
    )
    tokens: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert "access_token_csrf" in tokens
    assert "refresh_token" in tokens
    assert "refresh_token_csrf" in tokens


async def test_auth_login_testuser(client: AsyncClient) -> None:
    response: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": settings.TEST_NORMAL_USER,
            "password": settings.TEST_NORMAL_USER_PASSWORD,
        },
    )
    tokens: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert "access_token_csrf" in tokens
    assert "refresh_token" in tokens
    assert "refresh_token_csrf" in tokens


async def test_auth_login_random_user(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserPrincipals
    a_user_pass: str
    a_user, a_user_pass = await create_new_user(user_auth)
    response: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": a_user.email,
            "password": a_user_pass,
        },
    )
    tokens: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert "access_token_csrf" in tokens
    assert "refresh_token" in tokens
    assert "refresh_token_csrf" in tokens


async def test_auth_login_user_not_found(client: AsyncClient) -> None:
    not_username: str = random_email()
    password: str = random_lower_string()
    response: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": not_username,
            "password": password,
        },
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code >= 400
    assert "detail" in data
    assert data.get("detail") == ErrorCode.BAD_CREDENTIALS


async def test_auth_login_user_not_active(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    email: str = random_email()
    password: str = random_lower_string()
    a_user: User = await user_auth.users.create(
        schema=UserCreate(
            email=email,
            password=password,
            is_active=False,
            is_superuser=False,
            is_verified=False,
        )
    )
    response: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": a_user.email,
            "password": password,
        },
    )
    assert response.status_code >= 400
    data: Dict[str, Any] = response.json()
    assert "detail" in data
    assert data["detail"] == ErrorCode.USER_NOT_ACTIVE


async def test_auth_login_user_not_verified(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    settings.USERS_REQUIRE_VERIFICATION = True
    email: str = random_email()
    password: str = random_lower_string()
    a_user: User = await user_auth.users.create(
        schema=UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=False,
            is_verified=False,
        )
    )
    response: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": a_user.email,
            "password": password,
        },
    )
    assert response.status_code >= 400
    data: Dict[str, Any] = response.json()
    assert "detail" in data
    assert data["detail"] == ErrorCode.USER_NOT_VERIFIED
