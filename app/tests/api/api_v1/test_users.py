from typing import Dict

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.repositories.user import UsersRepository
from app.db.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string

pytestmark = pytest.mark.asyncio


async def test_get_users_superuser_me(
    client: AsyncClient, superuser_token_headers: Dict[str, str]
) -> None:
    response = await client.get("users/me", headers=superuser_token_headers)
    assert response.status_code == 200
    current_user = response.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


async def test_get_users_testuser_me(
    client: AsyncClient, testuser_token_headers: Dict[str, str]
) -> None:
    response = await client.get("users/me", headers=testuser_token_headers)
    assert response.status_code == 200
    current_user = response.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.TEST_NORMAL_USER


async def test_create_user_new_email(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    response = await client.post(
        "auth/register", headers=superuser_token_headers, json=data
    )
    assert 200 <= response.status_code < 300
    created_user = response.json()
    assert created_user["email"] == username

    users_repo = UsersRepository(session=db_session)
    user = await users_repo.read_by_email(username)
    assert user
    assert user.email == created_user["email"]


async def test_get_existing_user(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    username = random_email()
    password = random_lower_string()
    users_repo = UsersRepository(session=db_session)
    user = await users_repo.create(UserCreate(email=username, password=password))
    user_id = str(user.id)
    fetched_user = None
    response = await client.get(
        f"users/{user_id}",
        headers=superuser_token_headers,
    )
    fetched_user = response.json()
    assert 200 <= response.status_code < 300
    assert fetched_user
    existing_user = await users_repo.read_by_email(email=username)
    assert existing_user
    assert existing_user.email == fetched_user["email"]


async def test_create_user_existing_username(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    username = random_email()
    password = random_lower_string()
    users_repo = UsersRepository(session=db_session)
    user = await users_repo.create(UserCreate(email=username, password=password))
    data = {"email": username, "password": password}
    response = await client.post("users/", headers=superuser_token_headers, json=data)
    assert response.status_code >= 400
    created_user = response.json()
    assert "id" not in created_user


async def test_create_user_by_testuser(
    client: AsyncClient, testuser_token_headers: Dict[str, str]
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    response = await client.post(
        "users/",
        headers=testuser_token_headers,
        json=data,
    )
    assert response.status_code >= 400


async def test_list_users(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    users_repo = UsersRepository(session=db_session)
    username_1 = random_email()
    password_1 = random_lower_string()
    user_1 = await users_repo.create(UserCreate(email=username_1, password=password_1))
    username_2 = random_email()
    password_2 = random_lower_string()
    user_2 = await users_repo.create(UserCreate(email=username_2, password=password_2))
    response = await client.get("users/", headers=superuser_token_headers)
    assert 200 <= response.status_code < 300
    all_users = response.json()
    assert len(all_users) > 1
    for api_user in all_users:
        assert "email" in api_user
        if api_user["email"] == username_1:
            assert api_user["email"] == user_1.email
        if api_user["email"] == username_2:
            assert api_user["email"] == user_2.email
