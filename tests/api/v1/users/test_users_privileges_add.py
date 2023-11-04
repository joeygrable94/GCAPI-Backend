from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.users import create_random_user

from app.core.security.permissions.scope import AclPrivilege
from app.models.user import User
from app.schemas.user import UserReadAsAdmin, UserReadAsManager, UserUpdatePrivileges

pytestmark = pytest.mark.asyncio


async def test_add_user_priv_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user1: User = await create_random_user(db_session=db_session)
    test_priv = AclPrivilege("test:priv1")
    user1_update_priv: UserUpdatePrivileges = UserUpdatePrivileges(scopes=[test_priv])
    response: Response = await client.post(
        f"users/{user1.id}/privileges/add",
        headers=admin_token_headers,
        json=user1_update_priv.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    user1_new: UserReadAsAdmin = UserReadAsAdmin.model_validate(data)
    assert 200 <= response.status_code < 300
    response2: Response = await client.get(
        f"users/{user1_new.id}",
        headers=admin_token_headers,
    )
    assert 200 <= response2.status_code < 300
    data2: Dict[str, Any] = response2.json()
    user2_new: UserReadAsAdmin = UserReadAsAdmin.model_validate(data2)
    assert test_priv in user2_new.scopes


async def test_add_user_priv_as_manager(
    client: AsyncClient,
    db_session: AsyncSession,
    manager_token_headers: Dict[str, str],
) -> None:
    user1: User = await create_random_user(db_session=db_session)
    test_priv = AclPrivilege("test:priv1")
    user1_update_priv: UserUpdatePrivileges = UserUpdatePrivileges(scopes=[test_priv])
    response: Response = await client.post(
        f"users/{user1.id}/privileges/add",
        headers=manager_token_headers,
        json=user1_update_priv.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    user1_new: UserReadAsManager = UserReadAsManager.model_validate(data)
    assert 200 <= response.status_code < 300
    response2: Response = await client.get(
        f"users/{user1_new.id}",
        headers=manager_token_headers,
    )
    assert 200 <= response2.status_code < 300
    data2: Dict[str, Any] = response2.json()
    user2_new: UserReadAsManager = UserReadAsManager.model_validate(data2)
    assert test_priv in user2_new.scopes


async def test_add_user_priv_as_manager_add_role_disallowed(
    client: AsyncClient,
    db_session: AsyncSession,
    manager_token_headers: Dict[str, str],
) -> None:
    user1: User = await create_random_user(db_session=db_session)
    test_priv = AclPrivilege("role:admin")
    user1_update_priv: UserUpdatePrivileges = UserUpdatePrivileges(scopes=[test_priv])
    response: Response = await client.post(
        f"users/{user1.id}/privileges/add",
        headers=manager_token_headers,
        json=user1_update_priv.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert (
        data["detail"] == "You do not have permission to add role based access to users"
    )


async def test_add_user_priv_as_user_disallowed(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    user1: User = await create_random_user(db_session=db_session)
    test_priv = AclPrivilege("role:admin")
    user1_update_priv: UserUpdatePrivileges = UserUpdatePrivileges(scopes=[test_priv])
    response: Response = await client.post(
        f"users/{user1.id}/privileges/add",
        headers=employee_token_headers,
        json=user1_update_priv.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Insufficient permissions"
