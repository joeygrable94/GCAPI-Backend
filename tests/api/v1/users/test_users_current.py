from typing import Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import UserRepository
from app.models import User
from app.schemas.user import UserRead

pytestmark = pytest.mark.asyncio


async def test_read_current_user_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=admin_token_headers,
    )
    data: UserRead = UserRead.model_validate(response.json())
    assert 200 <= response.status_code < 300
    assert data.id
    user_repo: UserRepository = UserRepository(db_session)
    existing_data: User | None = await user_repo.read_by("auth_id", data.auth_id)
    assert existing_data
    assert existing_data.email == data.email


async def test_read_current_user_manager(
    client: AsyncClient,
    db_session: AsyncSession,
    manager_token_headers: Dict[str, str],
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=manager_token_headers,
    )
    data: UserRead = UserRead.model_validate(response.json())
    assert 200 <= response.status_code < 300
    assert data.id
    user_repo: UserRepository = UserRepository(db_session)
    existing_data: User | None = await user_repo.read_by("auth_id", data.auth_id)
    assert existing_data
    assert existing_data.email == data.email


async def test_read_current_user_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=employee_token_headers,
    )
    data: UserRead = UserRead.model_validate(response.json())
    assert 200 <= response.status_code < 300
    assert data.id
    user_repo: UserRepository = UserRepository(db_session)
    existing_data: User | None = await user_repo.read_by("auth_id", data.auth_id)
    assert existing_data
    assert existing_data.email == data.email


async def test_read_current_user_client(
    client: AsyncClient,
    db_session: AsyncSession,
    client_a_token_headers: Dict[str, str],
    client_b_token_headers: Dict[str, str],
) -> None:
    response_a: Response = await client.get(
        "users/me",
        headers=client_a_token_headers,
    )
    response_b: Response = await client.get(
        "users/me",
        headers=client_b_token_headers,
    )
    data_a: UserRead = UserRead.model_validate(response_a.json())
    data_b: UserRead = UserRead.model_validate(response_b.json())
    assert 200 <= response_a.status_code < 300
    assert data_a.id
    assert data_b.id
    user_repo: UserRepository = UserRepository(db_session)
    existing_data: User | None = await user_repo.read_by("auth_id", data_a.auth_id)
    assert existing_data
    assert existing_data.email == data_a.email


async def test_read_current_user_verified(
    client: AsyncClient,
    db_session: AsyncSession,
    user_verified_token_headers: Dict[str, str],
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=user_verified_token_headers,
    )
    data: UserRead = UserRead.model_validate(response.json())
    assert 200 <= response.status_code < 300
    assert data.id
    user_repo: UserRepository = UserRepository(db_session)
    existing_data: User | None = await user_repo.read_by("auth_id", data.auth_id)
    assert existing_data
    assert existing_data.email == data.email


async def test_read_current_user_unverified(
    client: AsyncClient,
    db_session: AsyncSession,
    user_unverified_token_headers: Dict[str, str],
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=user_unverified_token_headers,
    )
    data: UserRead = UserRead.model_validate(response.json())
    assert 200 <= response.status_code < 300
    assert data.id
    user_repo: UserRepository = UserRepository(db_session)
    existing_data: User | None = await user_repo.read_by("auth_id", data.auth_id)
    assert existing_data
    assert existing_data.email == data.email
