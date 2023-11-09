from typing import Any
from typing import Dict

import pytest
from httpx import AsyncClient
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.users import create_random_user

from app.core.security.permissions.scope import AclPrivilege
from app.models.user import User
from app.schemas.user import UserReadAsAdmin
from app.schemas.user import UserReadAsManager
from app.schemas.user import UserUpdatePrivileges

pytestmark = pytest.mark.asyncio


async def test_remove_user_priv_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    test_priv1 = AclPrivilege("test:priv1")
    test_priv2 = AclPrivilege("test:priv2")
    user1: User = await create_random_user(
        db_session=db_session, scopes=[test_priv1, test_priv2]
    )
    user1_remove_priv: UserUpdatePrivileges = UserUpdatePrivileges(scopes=[test_priv2])
    response: Response = await client.post(
        f"users/{user1.id}/privileges/remove",
        headers=admin_token_headers,
        json=user1_remove_priv.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    user1_new: UserReadAsAdmin = UserReadAsAdmin.model_validate(data)
    assert 200 <= response.status_code < 300
    assert test_priv1 in user1_new.scopes
    assert test_priv2 not in user1_new.scopes


async def test_remove_user_priv_as_manager(
    client: AsyncClient,
    db_session: AsyncSession,
    manager_token_headers: Dict[str, str],
) -> None:
    test_priv1 = AclPrivilege("test:priv1")
    test_priv2 = AclPrivilege("test:priv2")
    user1: User = await create_random_user(
        db_session=db_session, scopes=[test_priv1, test_priv2]
    )
    user1_remove_priv: UserUpdatePrivileges = UserUpdatePrivileges(scopes=[test_priv2])
    response: Response = await client.post(
        f"users/{user1.id}/privileges/remove",
        headers=manager_token_headers,
        json=user1_remove_priv.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    user1_new: UserReadAsManager = UserReadAsManager.model_validate(data)
    assert 200 <= response.status_code < 300
    assert test_priv1 in user1_new.scopes
    assert test_priv2 not in user1_new.scopes


async def test_remove_user_priv_as_manager_add_role_disallowed(
    client: AsyncClient,
    db_session: AsyncSession,
    manager_token_headers: Dict[str, str],
) -> None:
    test_priv1 = AclPrivilege("test:priv1")
    test_priv2 = AclPrivilege("test:priv2")
    test_role1 = AclPrivilege("role:client")
    user1: User = await create_random_user(
        db_session=db_session, scopes=[test_role1, test_priv1, test_priv2]
    )
    user1_remove_priv: UserUpdatePrivileges = UserUpdatePrivileges(scopes=[test_role1])
    response: Response = await client.post(
        f"users/{user1.id}/privileges/remove",
        headers=manager_token_headers,
        json=user1_remove_priv.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert (
        data["detail"]
        == "You do not have permission to remove role based access to users"
    )


async def test_remove_user_priv_as_user_disallowed(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    test_priv1 = AclPrivilege("test:priv1")
    test_priv2 = AclPrivilege("test:priv2")
    user1: User = await create_random_user(
        db_session=db_session, scopes=[test_priv1, test_priv2]
    )
    user1_remove_priv: UserUpdatePrivileges = UserUpdatePrivileges(scopes=[test_priv2])
    response: Response = await client.post(
        f"users/{user1.id}/privileges/remove",
        headers=employee_token_headers,
        json=user1_remove_priv.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Insufficient permissions"
