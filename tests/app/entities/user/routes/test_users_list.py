from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_PAGINATION,
)
from tests.constants.schema import ClientAuthorizedUser

pytestmark = pytest.mark.asyncio


async def test_list_all_users_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "users/",
        headers=admin_user.token_headers,
    )
    data = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == 7
    assert data["size"] == 1000
    assert len(data["results"]) == 7
    for entry in data["results"]:
        assert "id" in entry
        assert "auth_id" in entry
        assert "email" in entry
        assert "is_active" in entry
        assert "is_verified" in entry
        assert "is_superuser" in entry
        assert "scopes" in entry


async def test_list_all_users_as_manager(
    client: AsyncClient,
    db_session: AsyncSession,
    manager_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "users/",
        headers=manager_user.token_headers,
    )
    data = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == 7
    assert data["size"] == 1000
    assert len(data["results"]) == 7
    for entry in data["results"]:
        assert "id" in entry
        assert "auth_id" in entry
        assert "email" in entry
        assert "is_active" in entry
        assert "is_verified" in entry
        assert "scopes" in entry
        assert "is_superuser" not in entry


async def test_list_all_users_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "users/",
        headers=employee_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert data["detail"] == ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_PAGINATION
    assert response.status_code == 405
