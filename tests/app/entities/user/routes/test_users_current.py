from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.auth.constants import ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED
from app.entities.core_user.crud import UserRepository
from app.entities.core_user.schemas import UserRead, UserReadAsAdmin, UserReadAsManager
from tests.constants.schema import ClientAuthorizedUser

pytestmark = pytest.mark.asyncio


async def test_read_current_user_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=admin_user.token_headers,
    )
    data = UserReadAsAdmin.model_validate(response.json())
    assert 200 <= response.status_code < 300
    assert data.id
    user_repo = UserRepository(db_session)
    existing_data = await user_repo.read_by("auth_id", data.auth_id)
    assert existing_data
    assert existing_data.email == data.email


async def test_read_current_user_manager(
    client: AsyncClient,
    db_session: AsyncSession,
    manager_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=manager_user.token_headers,
    )
    data = UserReadAsManager.model_validate(response.json())
    assert 200 <= response.status_code < 300
    assert data.id
    user_repo = UserRepository(db_session)
    existing_data = await user_repo.read_by("auth_id", data.auth_id)
    assert existing_data
    assert existing_data.email == data.email


async def test_read_current_user_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=employee_user.token_headers,
    )
    data = UserRead.model_validate(response.json())
    assert 200 <= response.status_code < 300
    assert data.id
    user_repo = UserRepository(db_session)
    existing_data = await user_repo.read_by("auth_id", data.auth_id)
    assert existing_data
    assert existing_data.email == data.email


async def test_read_current_user_organization(
    client: AsyncClient,
    db_session: AsyncSession,
    client_a_user: ClientAuthorizedUser,
    client_b_user: ClientAuthorizedUser,
) -> None:
    response_a: Response = await client.get(
        "users/me",
        headers=client_a_user.token_headers,
    )
    response_b: Response = await client.get(
        "users/me",
        headers=client_b_user.token_headers,
    )
    data_a = UserRead.model_validate(response_a.json())
    data_b = UserRead.model_validate(response_b.json())
    assert 200 <= response_a.status_code < 300
    assert data_a.id
    assert data_b.id
    user_repo = UserRepository(db_session)
    existing_data = await user_repo.read_by("auth_id", data_a.auth_id)
    assert existing_data
    assert existing_data.email == data_a.email


async def test_read_current_user_verified(
    client: AsyncClient,
    db_session: AsyncSession,
    verified_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=verified_user.token_headers,
    )
    data = UserRead.model_validate(response.json())
    assert 200 <= response.status_code < 300
    assert data.id
    user_repo = UserRepository(db_session)
    existing_data = await user_repo.read_by("auth_id", data.auth_id)
    assert existing_data
    assert existing_data.email == data.email


async def test_read_current_user_unverified(
    client: AsyncClient,
    db_session: AsyncSession,
    unverified_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=unverified_user.token_headers,
    )
    json_data: dict[str, Any] = response.json()
    assert response.status_code == 403
    assert json_data["detail"] == ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED
