from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.core.security.permissions.scope import AclPrivilege
from app.models import User
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.users import create_random_user

pytestmark = pytest.mark.asyncio


async def test_add_user_priv_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    user1: User = await create_random_user(db_session=db_session)
    test_priv = AclPrivilege("test:priv1")
    user1_update_priv: dict[str, Any] = {"scopes": [test_priv]}
    response: Response = await client.post(
        f"users/{user1.id}/privileges/add",
        headers=admin_user.token_headers,
        json=user1_update_priv,
    )
    assert 200 <= response.status_code < 300
    data: dict[str, Any] = response.json()
    assert test_priv in data["scopes"]


async def test_add_user_priv_as_manager(
    client: AsyncClient,
    db_session: AsyncSession,
    manager_user: ClientAuthorizedUser,
) -> None:
    user1: User = await create_random_user(db_session=db_session)
    test_priv = AclPrivilege("test:priv1")
    user1_update_priv: dict[str, Any] = {"scopes": [test_priv]}
    response: Response = await client.post(
        f"users/{user1.id}/privileges/add",
        headers=manager_user.token_headers,
        json=user1_update_priv,
    )
    assert 200 <= response.status_code < 300
    data: dict[str, Any] = response.json()
    assert test_priv in data["scopes"]


async def test_add_user_priv_as_manager_add_role_disallowed(
    client: AsyncClient,
    db_session: AsyncSession,
    manager_user: ClientAuthorizedUser,
) -> None:
    user1: User = await create_random_user(db_session=db_session)
    test_priv = AclPrivilege("role:admin")
    user1_update_priv: dict[str, Any] = {"scopes": [test_priv]}
    response: Response = await client.post(
        f"users/{user1.id}/privileges/add",
        headers=manager_user.token_headers,
        json=user1_update_priv,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 405
    assert data["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_SCOPE_ADD


async def test_add_user_priv_as_user_disallowed(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_user: ClientAuthorizedUser,
) -> None:
    user1: User = await create_random_user(db_session=db_session)
    test_priv = AclPrivilege("role:admin")
    user1_update_priv: dict[str, Any] = {"scopes": [test_priv]}
    response: Response = await client.post(
        f"users/{user1.id}/privileges/add",
        headers=employee_user.token_headers,
        json=user1_update_priv,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 403
    assert data["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS
