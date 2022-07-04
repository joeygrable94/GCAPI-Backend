from typing import Any, Dict, Optional

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.api.exceptions import UserNotExists
from app.core.security.manager import UserManager
from app.db.repositories.user import UsersRepository
from app.db.schemas.user import UserCreate, UserRead, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string

pytestmark = pytest.mark.asyncio


'''
async def test_list_users_as_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    users_repo: UsersRepository = UsersRepository(session=db_session)
    username_1: str = random_email()
    password_1: str = random_lower_string()
    user_1: Any = await users_repo.create(
        UserCreate(email=username_1, password=password_1)
    )
    username_2: str = random_email()
    password_2: str = random_lower_string()
    user_2: Any = await users_repo.create(
        UserCreate(email=username_2, password=password_2)
    )
    response: Response = await client.get("users/", headers=superuser_token_headers)
    assert 200 <= response.status_code < 300
    all_users: Any = response.json()
    assert len(all_users) > 1
    for api_user in all_users:
        assert "email" in api_user
        if api_user["email"] == username_1:
            assert api_user["email"] == user_1.email
        if api_user["email"] == username_2:
            assert api_user["email"] == user_2.email


async def test_list_users_as_testuser(
    client: AsyncClient,
    testuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    users_repo: UsersRepository = UsersRepository(session=db_session)
    username_1: str = random_email()
    password_1: str = random_lower_string()
    user_1: Optional[UserRead] = await users_repo.create(  # noqa: F841
        UserCreate(email=username_1, password=password_1)
    )
    username_2: str = random_email()
    password_2: str = random_lower_string()
    user_2: Optional[UserRead] = await users_repo.create(  # noqa: F841
        UserCreate(email=username_2, password=password_2)
    )
    response: Response = await client.get("users/", headers=testuser_token_headers)
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == "Forbidden"
'''


async def test_get_current_superuser(
    client: AsyncClient, superuser_token_headers: Dict[str, str]
) -> None:
    response: Response = await client.get("users/me", headers=superuser_token_headers)
    assert response.status_code == 200
    current_user: Dict[str, Any] = response.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


async def test_get_current_testuser(
    client: AsyncClient, testuser_token_headers: Dict[str, str]
) -> None:
    response: Response = await client.get("users/me", headers=testuser_token_headers)
    assert response.status_code == 200
    current_user: Dict[str, Any] = response.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.TEST_NORMAL_USER


'''
async def test_update_current_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    response: Response = await client.get("users/me", headers=superuser_token_headers)
    super_me: Any = response.json()
    new_password: str = random_lower_string()
    users_repo: UsersRepository = UsersRepository(session=db_session)
    super_me_updated: Any = await users_repo.update(
        user_id=super_me["id"], schema=UserUpdate(password=new_password)
    )
    assert super_me["id"] == str(super_me_updated.id)


async def test_update_current_testuser(
    client: AsyncClient,
    testuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    response: Response = await client.get("users/me", headers=testuser_token_headers)
    test_me: Any = response.json()
    new_password: str = random_lower_string()
    users_repo: UsersRepository = UsersRepository(session=db_session)
    test_me_updated: Any = await users_repo.update(
        user_id=test_me["id"], schema=UserUpdate(password=new_password)
    )
    assert test_me["id"] == str(test_me_updated.id)


async def test_get_user_by_id_as_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    users_repo: UsersRepository = UsersRepository(session=db_session)
    user: Any = await users_repo.create(UserCreate(email=username, password=password))
    response: Response = await client.get(
        f"users/{user.id}",
        headers=superuser_token_headers,
    )
    fetched_user: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert fetched_user
    existing_user: Any = await users_repo.read_by_email(email=username)
    assert existing_user
    assert existing_user.email == fetched_user["email"]


async def test_get_user_by_id_as_testuser(
    client: AsyncClient,
    testuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    users_repo: UsersRepository = UsersRepository(session=db_session)
    user: Any = await users_repo.create(UserCreate(email=username, password=password))
    response: Response = await client.get(
        f"users/{user.id}",
        headers=testuser_token_headers,
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == "Forbidden"


async def test_delete_user_by_id_as_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    users_repo: UsersRepository = UsersRepository(session=db_session)
    user: Any = await users_repo.create(UserCreate(email=username, password=password))
    response: Response = await client.delete(
        f"users/{user.id}",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    with pytest.raises(UserNotExists):
        user_not_found: Any = await users_repo.read_by_email(email=username)
        assert user_not_found is None


async def test_delete_user_by_id_as_testuser(
    client: AsyncClient,
    testuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    users_repo: UsersRepository = UsersRepository(session=db_session)
    user: Any = await users_repo.create(UserCreate(email=username, password=password))
    response: Response = await client.delete(
        f"users/{user.id}",
        headers=testuser_token_headers,
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == "Forbidden"
'''
