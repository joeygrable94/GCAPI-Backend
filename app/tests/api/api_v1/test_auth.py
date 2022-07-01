from typing import Any, Dict, Optional

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.repositories.user import UsersRepository
from app.db.schemas.user import UserCreate, UserRead
from app.tests.utils.utils import random_email, random_lower_string

pytestmark = pytest.mark.asyncio


async def test_auth_login_superuser(client: AsyncClient) -> None:
    r: Response = await client.post(
        "auth/jwt/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        },
    )
    tokens: Dict[str, Any] = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens


async def test_auth_login_testuser(client: AsyncClient) -> None:
    r: Response = await client.post(
        "auth/jwt/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": settings.TEST_NORMAL_USER,
            "password": settings.TEST_NORMAL_USER_PASSWORD,
        },
    )
    tokens: Dict[str, Any] = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens


async def test_auth_logout_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    r: Response = await client.post("auth/jwt/logout", headers=superuser_token_headers)
    data: Optional[Dict[str, Any]] = r.json()
    assert r.status_code == 200
    assert data is None


async def test_auth_logout_testuser(
    client: AsyncClient, testuser_token_headers: Dict[str, str]
) -> None:
    r: Response = await client.post("auth/jwt/logout", headers=testuser_token_headers)
    data: Optional[Dict[str, Any]] = r.json()
    assert r.status_code == 200
    assert data is None


async def test_auth_register_user_as_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    data: Dict[str, str] = {"email": username, "password": password}
    response: Response = await client.post(
        "auth/register", headers=superuser_token_headers, json=data
    )
    assert 200 <= response.status_code < 300
    created_user: Dict[str, Any] = response.json()
    assert created_user["email"] == username

    users_repo: UsersRepository = UsersRepository(session=db_session)
    user: Optional[UserRead] = await users_repo.read_by_email(username)
    assert user
    assert user.email == created_user["email"]


async def test_auth_register_user_as_testuser(
    client: AsyncClient, testuser_token_headers: Dict[str, str]
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    data: Dict[str, str] = {"email": username, "password": password}
    response: Response = await client.post(
        "users/",
        headers=testuser_token_headers,
        json=data,
    )
    assert response.status_code >= 400


async def test_auth_register_user_as_superuser_existing_username(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    users_repo: UsersRepository = UsersRepository(session=db_session)
    user: Optional[UserRead] = await users_repo.create(  # noqa: F841
        UserCreate(email=username, password=password)
    )
    data: Dict[str, str] = {"email": username, "password": password}
    response: Response = await client.post(
        "users/", headers=superuser_token_headers, json=data
    )
    assert response.status_code >= 400
    created_user: Dict[str, Any] = response.json()
    assert "id" not in created_user
