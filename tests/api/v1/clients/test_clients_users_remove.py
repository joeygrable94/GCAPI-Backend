from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.users import create_random_user

from app.api.exceptions.errors import ErrorCode
from app.core.utilities import get_uuid_str
from app.schemas import UserClientRead

pytestmark = pytest.mark.asyncio


async def test_clients_remove_user_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user = await create_random_user(db_session)
    a_client = await create_random_client(db_session)
    user_client_rel = await assign_user_to_client(db_session, a_user, a_client)
    user_client_in = {"user_id": str(a_user.id), "client_id": str(a_client.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/remove/user",
        headers=admin_token_headers,
        json=user_client_in,
    )
    assert 200 <= response.status_code < 300
    user_client_read = UserClientRead(**response.json())
    assert user_client_read.id is not None
    assert user_client_read.user_id == user_client_rel.user_id
    assert user_client_read.client_id == user_client_rel.client_id


async def test_clients_remove_user_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user = await create_random_user(db_session)
    a_client = await create_random_client(db_session)
    user_client_rel = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    user_client_in = {"user_id": str(a_user.id), "client_id": str(a_client.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/remove/user",
        headers=employee_token_headers,
        json=user_client_in,
    )
    assert response.status_code == 403
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS


async def test_clients_remove_user_as_superuser_missmatching_client_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user = await create_random_user(db_session)
    a_client_bad_id = get_uuid_str()
    a_client = await create_random_client(db_session)
    user_client_rel = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    user_client_in = {"user_id": str(a_user.id), "client_id": a_client_bad_id}
    response: Response = await client.post(
        f"clients/{a_client.id}/remove/user",
        headers=admin_token_headers,
        json=user_client_in,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_clients_remove_user_as_superuser_user_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user = await create_random_user(db_session)
    a_user_bad_id = get_uuid_str()
    a_client = await create_random_client(db_session)
    user_client_rel = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    user_client_in = {"user_id": a_user_bad_id, "client_id": str(a_client.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/remove/user",
        headers=admin_token_headers,
        json=user_client_in,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.USER_NOT_FOUND


async def test_clients_remove_user_as_superuser_relation_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user = await create_random_user(db_session)
    a_client = await create_random_client(db_session)
    user_client_in = {"user_id": str(a_user.id), "client_id": str(a_client.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/remove/user",
        headers=admin_token_headers,
        json=user_client_in,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.CLIENT_RELATIONSHOP_NOT_FOUND
