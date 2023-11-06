from typing import Any, Dict, List

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.core.config import settings
from app.core.utilities.uuids import get_uuid_str
from app.crud import UserRepository
from app.models import User

pytestmark = pytest.mark.asyncio


async def test_read_all_users_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user_repo: UserRepository = UserRepository(db_session)
    users: List[User] | List[None] | None = await user_repo.list(1)
    if users and len(users) > 0:
        for user in users:
            if user is not None:
                response: Response = await client.get(
                    f"users/{user.id}",
                    headers=admin_token_headers,
                )
                data: Dict[str, Any] = response.json()
                assert 200 <= response.status_code < 300
                assert data["id"] == str(user.id)
                assert data.get("scopes") is not None
                assert data.get("is_superuser") is not None


async def test_read_all_users_as_manager(
    client: AsyncClient,
    db_session: AsyncSession,
    manager_token_headers: Dict[str, str],
) -> None:
    user_repo: UserRepository = UserRepository(db_session)
    users: List[User] | List[None] | None = await user_repo.list(1)
    if users and len(users) > 0:
        for user in users:
            if user is not None:
                response: Response = await client.get(
                    f"users/{user.id}",
                    headers=manager_token_headers,
                )
                data: Dict[str, Any] = response.json()
                assert 200 <= response.status_code < 300
                assert data["id"] == str(user.id)
                assert data.get("scopes") is not None
                assert data.get("is_superuser") is None


async def test_read_user_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
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
        headers=employee_token_headers,
    )
    data_a: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data_a["id"] == str(user_employee.id)
    assert data_a.get("scopes") is None
    assert data_a.get("is_superuser") is None
    # cannot access other users
    response_b: Response = await client.get(
        f"users/{user_client_a.id}",
        headers=employee_token_headers,
    )
    data_b: Dict[str, Any] = response_b.json()
    assert data_b["detail"] == "Insufficient permissions"
    assert response_b.status_code == 403


async def test_read_user_as_user_verified(
    client: AsyncClient,
    db_session: AsyncSession,
    user_verified_token_headers: Dict[str, str],
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
        headers=user_verified_token_headers,
    )
    data_a: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data_a["id"] == str(user_verified.id)
    assert data_a.get("scopes") is None
    assert data_a.get("is_superuser") is None
    # cannot access other users
    response_b: Response = await client.get(
        f"users/{user_employee.id}",
        headers=user_verified_token_headers,
    )
    data_b: Dict[str, Any] = response_b.json()
    assert data_b["detail"] == "Insufficient permissions"
    assert response_b.status_code == 403


async def test_read_user_by_id_as_admin_id_invalid(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_id = get_uuid_str()
    response: Response = await client.get(
        f"users/{fake_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.USER_NOT_FOUND
