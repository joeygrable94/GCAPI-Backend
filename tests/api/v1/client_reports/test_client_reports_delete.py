from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.client_reports import create_random_client_report
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.users import get_user_by_email

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.models import User, UserClient
from app.schemas import ClientRead, ClientReportRead

pytestmark = pytest.mark.asyncio


async def test_delete_client_report_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry: ClientReportRead = await create_random_client_report(
        db_session, client_id=a_client.id
    )
    response: Response = await client.delete(
        f"clients/reports/{a_client.id}/{entry.id}",
        headers=admin_token_headers,
    )
    assert 200 <= response.status_code < 300
    response: Response = await client.get(
        f"clients/reports/{a_client.id}/{entry.id}",
        headers=admin_token_headers,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.CLIENT_REPORT_NOT_FOUND


async def test_delete_client_report_by_id_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_employee
    )
    a_client: ClientRead = await create_random_client(db_session)
    a_user_client: UserClient = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    entry: ClientReportRead = await create_random_client_report(
        db_session, client_id=a_client.id
    )
    response: Response = await client.delete(
        f"clients/reports/{a_client.id}/{entry.id}",
        headers=employee_token_headers,
    )
    assert 200 <= response.status_code < 300
    response: Response = await client.get(
        f"clients/reports/{a_client.id}/{entry.id}",
        headers=employee_token_headers,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.CLIENT_REPORT_NOT_FOUND
