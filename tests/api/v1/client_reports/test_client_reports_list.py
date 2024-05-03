from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.client_reports import create_random_client_report
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.users import get_user_by_email

from app.core.config import settings
from app.models import User, UserClient
from app.schemas import ClientRead, ClientReportRead

pytestmark = pytest.mark.asyncio


async def test_list_all_client_reports_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_1: ClientReportRead = await create_random_client_report(
        db_session, client_id=a_client.id
    )
    entry_2: ClientReportRead = await create_random_client_report(
        db_session, client_id=a_client.id
    )
    entry_3: ClientReportRead = await create_random_client_report(
        db_session, client_id=a_client.id
    )
    entry_4: ClientReportRead = await create_random_client_report(
        db_session, client_id=a_client.id
    )
    response: Response = await client.get(
        f"clients/reports/{a_client.id}",
        headers=admin_token_headers,
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert data["page"] == 1
    assert data["total"] == 4
    assert data["size"] == 1000
    assert len(data["results"]) == 4
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["title"] == entry_1.title
            assert entry["url"] == entry_1.url
            assert entry["description"] == entry_1.description
            assert entry["keys"] == entry_1.keys
            assert entry["client_id"] == str(entry_1.client_id)
        if entry["id"] == str(entry_2.id):
            assert entry["title"] == entry_2.title
            assert entry["url"] == entry_2.url
            assert entry["description"] == entry_2.description
            assert entry["keys"] == entry_2.keys
            assert entry["client_id"] == str(entry_2.client_id)
        if entry["id"] == str(entry_3.id):
            assert entry["title"] == entry_3.title
            assert entry["url"] == entry_3.url
            assert entry["description"] == entry_3.description
            assert entry["keys"] == entry_3.keys
            assert entry["client_id"] == str(entry_3.client_id)
        if entry["id"] == str(entry_4.id):
            assert entry["title"] == entry_4.title
            assert entry["url"] == entry_4.url
            assert entry["description"] == entry_4.description
            assert entry["keys"] == entry_4.keys
            assert entry["client_id"] == str(entry_4.client_id)


async def test_list_all_client_reports_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_user_client: UserClient = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    entry_1: ClientReportRead = await create_random_client_report(  # noqa: F841
        db_session, client_id=a_client.id
    )
    entry_2: ClientReportRead = await create_random_client_report(  # noqa: F841
        db_session, client_id=a_client.id
    )
    entry_3: ClientReportRead = await create_random_client_report(
        db_session, client_id=b_client.id
    )
    entry_4: ClientReportRead = await create_random_client_report(
        db_session, client_id=b_client.id
    )
    response: Response = await client.get(
        f"clients/reports/{a_client.id}",
        headers=employee_token_headers,
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert data["page"] == 1
    assert data["total"] == 2
    assert data["size"] == 1000
    assert len(data["results"]) == 2
    for entry in data["results"]:
        if entry["id"] == str(entry_3.id):
            assert entry["title"] == entry_3.title
            assert entry["url"] == entry_3.url
            assert entry["description"] == entry_3.description
            assert entry["keys"] == entry_3.keys
            assert entry["client_id"] == str(entry_3.client_id)
        if entry["id"] == str(entry_4.id):
            assert entry["title"] == entry_4.title
            assert entry["url"] == entry_4.url
            assert entry["description"] == entry_4.description
            assert entry["keys"] == entry_4.keys
            assert entry["client_id"] == str(entry_4.client_id)
