from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.client_reports import create_random_client_report
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.notes import create_random_note
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_boolean, random_lower_string

from app.api.exceptions.errors import ErrorCode
from app.core.config import settings
from app.models import User, UserClient
from app.schemas import ClientRead, ClientReportRead, NoteRead

pytestmark = pytest.mark.asyncio


async def test_create_client_report_note_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_admin)
    a_client: ClientRead = await create_random_client(db_session)
    a_report: ClientReportRead = await create_random_client_report(
        db_session, client_id=a_client.id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        description=random_lower_string(),
        is_active=random_boolean(),
        user_id=str(a_user.id),
    )
    response: Response = await client.post(
        f"clients/reports/{a_client.id}/{a_report.id}/notes",
        headers=admin_token_headers,
        json=data_in,
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert data["title"] == data_in["title"]
    assert data["description"] == data_in["description"]
    assert data["is_active"] == data_in["is_active"]
    assert data["user_id"] == data_in["user_id"]


async def test_create_client_report_note_as_superuser_note_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_admin)
    b_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    a_note: NoteRead = await create_random_note(db_session, user_id=b_user.id)
    a_report: ClientReportRead = await create_random_client_report(
        db_session, client_id=a_client.id
    )
    data_in: Dict[str, Any] = dict(
        title=a_note.title,
        description=random_lower_string(),
        is_active=random_boolean(),
        user_id=str(a_user.id),
    )
    response: Response = await client.post(
        f"clients/reports/{a_client.id}/{a_report.id}/notes",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 400
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.NOTE_EXISTS


async def test_create_client_report_note_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    a_user_a_client: UserClient = await assign_user_to_client(
        db_session, a_user, a_client
    )
    a_report: ClientReportRead = await create_random_client_report(
        db_session, client_id=a_user_a_client.client_id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        description=random_lower_string(),
        is_active=random_boolean(),
        user_id=str(a_user.id),
    )
    response: Response = await client.post(
        f"clients/reports/{a_client.id}/{a_report.id}/notes",
        headers=employee_token_headers,
        json=data_in,
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert data["title"] == data_in["title"]
    assert data["description"] == data_in["description"]
    assert data["is_active"] == data_in["is_active"]
    assert data["user_id"] == data_in["user_id"]


async def test_create_client_report_note_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    a_report: ClientReportRead = await create_random_client_report(
        db_session, client_id=a_client.id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        description=random_lower_string(),
        is_active=random_boolean(),
        user_id=str(a_user.id),
    )
    response: Response = await client.post(
        f"clients/reports/{a_client.id}/{a_report.id}/notes",
        headers=employee_token_headers,
        json=data_in,
    )
    assert response.status_code == 405
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS
