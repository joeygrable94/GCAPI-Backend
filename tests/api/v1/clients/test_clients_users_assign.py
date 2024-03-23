from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.users import get_user_by_email

from app.api.exceptions.errors import ErrorCode
from app.core.config import settings
from app.core.utilities.uuids import get_uuid_str
from app.schemas.user_client import UserClientRead

pytestmark = pytest.mark.asyncio


async def test_clients_assign_user_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    an_admin = await get_user_by_email(db_session, settings.auth.first_admin)
    a_client = await create_random_client(db_session)
    user_client_in = {"user_id": str(an_admin.id), "client_id": str(a_client.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/assign/user",
        headers=admin_token_headers,
        json=user_client_in,
    )
    assert 200 <= response.status_code < 300
    user_client_read = UserClientRead(**response.json())
    assert user_client_read.id is not None
    assert user_client_read.user_id == an_admin.id
    assert user_client_read.client_id == a_client.id


async def test_clients_assign_user_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_employee = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client = await create_random_client(db_session)
    user_client_in = {"user_id": str(a_employee.id), "client_id": str(a_client.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/assign/user",
        headers=employee_token_headers,
        json=user_client_in,
    )
    assert response.status_code == 403
    data: Dict[str, Any] = response.json()
    assert data["detail"] == "Insufficient permissions"


async def test_clients_assign_user_as_superuser_missmatching_client_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    an_admin = await get_user_by_email(db_session, settings.auth.first_admin)
    a_client_bad_id = get_uuid_str()
    a_client = await create_random_client(db_session)
    user_client_in = {"user_id": str(an_admin.id), "client_id": a_client_bad_id}
    response: Response = await client.post(
        f"clients/{a_client.id}/assign/user",
        headers=admin_token_headers,
        json=user_client_in,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_clients_assign_user_as_superuser_user_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user_id = get_uuid_str()
    a_client = await create_random_client(db_session)
    user_client_in = {"user_id": a_user_id, "client_id": str(a_client.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/assign/user",
        headers=admin_token_headers,
        json=user_client_in,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.USER_NOT_FOUND
