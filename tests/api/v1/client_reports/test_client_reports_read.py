from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.client_reports import create_random_client_report
from tests.utils.clients import create_random_client

from app.api.exceptions.errors import ErrorCode
from app.core.utilities import get_uuid_str
from app.schemas import ClientRead, ClientReportRead

pytestmark = pytest.mark.asyncio


async def test_read_client_report_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry: ClientReportRead = await create_random_client_report(
        db_session, client_id=a_client.id
    )
    response: Response = await client.get(
        f"clients/reports/{a_client.id}/{entry.id}",
        headers=admin_token_headers,
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert data["id"] == str(entry.id)
    assert data["title"] == entry.title
    assert data["url"] == entry.url
    assert data["description"] == entry.description
    assert data["keys"] == entry.keys
    assert data["client_id"] == str(entry.client_id)


async def test_read_client_report_by_id_as_superuser_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_report_id = get_uuid_str()
    a_client: ClientRead = await create_random_client(db_session)
    entry: ClientReportRead = await create_random_client_report(  # noqa: F841
        db_session, client_id=a_client.id
    )
    response: Response = await client.get(
        f"clients/reports/{a_client.id}/{fake_report_id}",
        headers=admin_token_headers,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.CLIENT_REPORT_NOT_FOUND
