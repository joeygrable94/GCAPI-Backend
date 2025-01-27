from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.core.config import settings
from app.core.utilities import get_uuid_str
from app.crud import UserRepository
from app.models import User
from tests.constants.schema import ClientAuthorizedUser

pytestmark = pytest.mark.asyncio


async def test_read_all_users_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    user_repo: UserRepository = UserRepository(db_session)
    users: list[User] | list[None] | None = await user_repo.get_list(1)
    if users and len(users) > 0:
        for user in users:
            if user is not None:
                response: Response = await client.get(
                    f"users/{user.id}",
                    headers=admin_user.token_headers,
                )
                data: dict[str, Any] = response.json()
                assert 200 <= response.status_code < 300
                assert data["id"] == str(user.id)
                assert data.get("scopes") is not None
                assert data.get("is_superuser") is not None


async def test_read_all_users_as_manager(
    client: AsyncClient,
    db_session: AsyncSession,
    manager_user: ClientAuthorizedUser,
) -> None:
    user_repo: UserRepository = UserRepository(db_session)
    users: list[User] | list[None] | None = await user_repo.get_list(1)
    if users and len(users) > 0:
        for user in users:
            if user is not None:
                response: Response = await client.get(
                    f"users/{user.id}",
                    headers=manager_user.token_headers,
                )
                data: dict[str, Any] = response.json()
                assert 200 <= response.status_code < 300
                assert data["id"] == str(user.id)
                assert data.get("scopes") is not None
                assert data.get("is_superuser") is None


async def test_read_user_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_user: ClientAuthorizedUser,
) -> None:
    user_repo: UserRepository = UserRepository(db_session)
    user_employee: User | None = await user_repo.read_by(
        "email", settings.auth.first_employee
    )
    user_client_a: User | None = await user_repo.read_by(
        "email", settings.auth.first_client_a
    )
    assert user_employee is not None
    assert user_client_a is not None
    # can access self
    response: Response = await client.get(
        f"users/{user_employee.id}",
        headers=employee_user.token_headers,
    )
    data_a: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data_a["id"] == str(user_employee.id)
    assert data_a.get("scopes") is None
    assert data_a.get("is_superuser") is None
    # cannot access other users
    response_b: Response = await client.get(
        f"users/{user_client_a.id}",
        headers=employee_user.token_headers,
    )
    data_b: dict[str, Any] = response_b.json()
    assert data_b["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS
    assert response_b.status_code == 403


async def test_read_user_as_user_verified(
    client: AsyncClient,
    db_session: AsyncSession,
    verified_user: ClientAuthorizedUser,
) -> None:
    user_repo: UserRepository = UserRepository(db_session)
    user_employee: User | None = await user_repo.read_by(
        "email", settings.auth.first_employee
    )
    user_verified: User | None = await user_repo.read_by(
        "email", settings.auth.first_user_verified
    )
    assert user_employee is not None
    assert user_verified is not None
    # can access self
    response: Response = await client.get(
        f"users/{user_verified.id}",
        headers=verified_user.token_headers,
    )
    data_a: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data_a["id"] == str(user_verified.id)
    assert data_a.get("scopes") is None
    assert data_a.get("is_superuser") is None
    # cannot access other users
    response_b: Response = await client.get(
        f"users/{user_employee.id}",
        headers=verified_user.token_headers,
    )
    data_b: dict[str, Any] = response_b.json()
    assert data_b["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS
    assert response_b.status_code == 403


async def test_read_user_by_id_as_admin_user_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    fake_id = get_uuid_str()
    response: Response = await client.get(
        f"users/{fake_id}",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.USER_NOT_FOUND


async def test_read_user_by_id_as_admin_id_invalid(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    fake_id = "FAKE-UUID-ASDF-1234567890"
    response: Response = await client.get(
        f"users/{fake_id}",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 422
    assert data["detail"] == ErrorCode.ID_INVALID
