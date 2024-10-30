from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.websites import create_random_website

from app.api.exceptions.errors import ErrorCode
from app.core.utilities import get_uuid_str
from app.schemas import ClientWebsiteRead

pytestmark = pytest.mark.asyncio


async def test_clients_assign_website_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_website = await create_random_website(db_session)
    a_client = await create_random_client(db_session)
    client_website = {"client_id": str(a_client.id), "website_id": str(a_website.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/assign/website",
        headers=admin_token_headers,
        json=client_website,
    )
    assert 200 <= response.status_code < 300
    user_client_read = ClientWebsiteRead(**response.json())
    assert user_client_read.id is not None
    assert user_client_read.client_id == a_client.id
    assert user_client_read.website_id == a_website.id


async def test_clients_assign_website_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_website = await create_random_website(db_session)
    a_client = await create_random_client(db_session)
    client_website = {"client_id": str(a_client.id), "website_id": str(a_website.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/assign/website",
        headers=employee_token_headers,
        json=client_website,
    )
    assert response.status_code == 403
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS


async def test_clients_assign_website_as_superuser_missmatching_client_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_website = await create_random_website(db_session)
    a_client_bad_id = get_uuid_str()
    a_client = await create_random_client(db_session)
    client_website = {"client_id": a_client_bad_id, "website_id": str(a_website.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/assign/website",
        headers=admin_token_headers,
        json=client_website,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_clients_assign_website_as_superuser_website_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_website_bad_id = get_uuid_str()
    a_client = await create_random_client(db_session)
    client_website = {"client_id": str(a_client.id), "website_id": a_website_bad_id}
    response: Response = await client.post(
        f"clients/{a_client.id}/assign/website",
        headers=admin_token_headers,
        json=client_website,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.WEBSITE_NOT_FOUND
