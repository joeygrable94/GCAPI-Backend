from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.users import create_random_user
from tests.utils.utils import random_email

from app.api.errors import ErrorCode
from app.db.schemas.user import UserAdmin
from app.security import AuthManager

pytestmark = pytest.mark.asyncio


async def test_update_add_user_permissions_as_superuser(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    new_role = "role:manager"
    update_data = {"email": a_user.email, "principals": [new_role]}
    response: Response = await client.patch(
        f"users/{a_user.id}/permissions/add",
        headers=superuser_token_headers,
        json=update_data,
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert "role:user" in updated_user["principals"]
    assert f"user:{a_user.email}" in updated_user["principals"]
    assert new_role in updated_user["principals"]


async def test_update_add_user_permissions_as_superuser_invalid_scope_format(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    bad_role = "invalid_scope"
    update_data = {"email": a_user.email, "principals": [bad_role]}
    response: Response = await client.patch(
        f"users/{a_user.id}/permissions/add",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert response.status_code == 422
    updated_user: Dict[str, Any] = response.json()
    assert updated_user["detail"][0]["msg"] == "invalid permission scope format"


async def test_update_add_user_permissions_as_testuser(
    client: AsyncClient,
    user_auth: AuthManager,
    testuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    new_role: str = "role:manager"
    update_data: Dict[str, Any] = {"email": a_user.email, "principals": [new_role]}
    response: Response = await client.patch(
        f"users/{a_user.id}/permissions/add",
        headers=testuser_token_headers,
        json=update_data,
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert updated_user["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS


async def test_update_add_user_permissions_as_superuser_email_invalid(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    fake_email: str = random_email()
    update_data: Dict[str, Any] = {"email": fake_email, "principals": ["role:manager"]}
    response: Response = await client.patch(
        f"users/{a_user.id}/permissions/add",
        headers=superuser_token_headers,
        json=update_data,
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 401
    assert updated_user["detail"] == "email must match the user to update"


async def test_update_remove_user_permissions_as_superuser(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    remove_role: str = "role:user"
    update_data: Dict[str, Any] = {"email": a_user.email, "principals": [remove_role]}
    response: Response = await client.patch(
        f"users/{a_user.id}/permissions/remove",
        headers=superuser_token_headers,
        json=update_data,
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert f"user:{a_user.email}" in updated_user["principals"]
    assert remove_role not in updated_user["principals"]


async def test_update_remove_user_permissions_as_testuser(
    client: AsyncClient,
    user_auth: AuthManager,
    testuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    remove_role: str = "role:user"
    update_data: Dict[str, Any] = {"email": a_user.email, "principals": [remove_role]}
    response: Response = await client.patch(
        f"users/{a_user.id}/permissions/remove",
        headers=testuser_token_headers,
        json=update_data,
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert updated_user["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS


async def test_update_remove_user_permissions_as_superuser_email_invalid(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    remove_role: str = "role:user"
    fake_email: str = random_email()
    update_data: Dict[str, Any] = {"email": fake_email, "principals": [remove_role]}
    response: Response = await client.patch(
        f"users/{a_user.id}/permissions/remove",
        headers=superuser_token_headers,
        json=update_data,
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 401
    assert updated_user["detail"] == "email must match the user to update"
