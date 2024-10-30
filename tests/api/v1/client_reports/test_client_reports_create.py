from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_domain, random_lower_string

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.core.utilities import get_uuid_str
from app.models import User
from app.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_create_client_report_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        url=f"{random_domain()}/{random_lower_string(6)}/{random_lower_string(6)}",
        description=random_lower_string(),
        keys=random_lower_string(),
        client_id=str(a_client.id),
    )
    response: Response = await client.post(
        f"clients/reports/{a_client.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["url"] == data_in["url"]
    assert entry["description"] == data_in["description"]
    assert entry["keys"] == data_in["keys"]
    assert entry["client_id"] == str(a_client.id)


async def test_create_client_report_by_id_as_superuser_client_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_client_id = get_uuid_str()
    a_client: ClientRead = await create_random_client(db_session)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        url=f"{random_domain()}/{random_lower_string(6)}/{random_lower_string(6)}",
        description=random_lower_string(),
        keys=random_lower_string(),
        client_id=fake_client_id,
    )
    response: Response = await client.post(
        f"clients/reports/{a_client.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_create_client_report_by_id_as_superuser_title_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        url=f"{random_domain()}/{random_lower_string(6)}/{random_lower_string(6)}",
        description=random_lower_string(),
        keys=random_lower_string(),
        client_id=str(a_client.id),
    )
    response: Response = await client.post(
        f"clients/reports/{a_client.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["url"] == data_in["url"]
    assert entry["description"] == data_in["description"]
    assert entry["keys"] == data_in["keys"]
    assert entry["client_id"] == str(a_client.id)
    data_in_2: Dict[str, Any] = dict(
        title=entry["title"],
        url=f"{random_domain()}/{random_lower_string(6)}/{random_lower_string(6)}",
        description=random_lower_string(),
        keys=random_lower_string(),
        client_id=str(a_client.id),
    )
    response_2: Response = await client.post(
        f"clients/reports/{a_client.id}",
        headers=admin_token_headers,
        json=data_in_2,
    )
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ErrorCode.CLIENT_REPORT_EXISTS


async def test_create_client_report_by_id_as_superuser_url_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        url=f"{random_domain()}/{random_lower_string(6)}/{random_lower_string(6)}",
        description=random_lower_string(),
        keys=random_lower_string(),
        client_id=str(a_client.id),
    )
    response: Response = await client.post(
        f"clients/reports/{a_client.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["url"] == data_in["url"]
    assert entry["description"] == data_in["description"]
    assert entry["keys"] == data_in["keys"]
    assert entry["client_id"] == str(a_client.id)
    data_in_2: Dict[str, Any] = dict(
        title=random_lower_string(),
        url=data_in["url"],
        description=random_lower_string(),
        keys=random_lower_string(),
        client_id=str(a_client.id),
    )
    response_2: Response = await client.post(
        f"clients/reports/{a_client.id}",
        headers=admin_token_headers,
        json=data_in_2,
    )
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ErrorCode.CLIENT_REPORT_EXISTS


async def test_create_client_report_by_id_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    a_user_a_client = await assign_user_to_client(db_session, a_user, a_client)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        url=f"{random_domain()}/{random_lower_string(6)}/{random_lower_string(6)}",
        description=random_lower_string(),
        keys=random_lower_string(),
        client_id=str(a_user_a_client.client_id),
    )
    response: Response = await client.post(
        f"clients/reports/{a_client.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["url"] == data_in["url"]
    assert entry["description"] == data_in["description"]
    assert entry["keys"] == data_in["keys"]
    assert entry["client_id"] == str(a_client.id)


async def test_create_client_report_by_id_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        url=f"{random_domain()}/{random_lower_string(6)}/{random_lower_string(6)}",
        description=random_lower_string(),
        keys=random_lower_string(),
        client_id=str(a_client.id),
    )
    response: Response = await client.post(
        f"clients/reports/{a_client.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS
