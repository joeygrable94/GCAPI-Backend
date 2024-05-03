from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.client_reports import (
    create_random_client_report,
    create_random_client_report_note,
)
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.notes import create_random_note
from tests.utils.users import get_user_by_email

from app.core.config import settings
from app.models import User, UserClient
from app.schemas import ClientRead, ClientReportNoteRead, ClientReportRead, NoteRead

pytestmark = pytest.mark.asyncio


async def test_list_all_client_report_notes_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_admin)
    a_client: ClientRead = await create_random_client(db_session)
    a_report: ClientReportRead = await create_random_client_report(
        db_session, client_id=a_client.id
    )
    note_1: NoteRead = await create_random_note(db_session, user_id=a_user.id)
    note_2: NoteRead = await create_random_note(db_session, user_id=a_user.id)
    note_3: NoteRead = await create_random_note(db_session, user_id=a_user.id)
    note_4: NoteRead = await create_random_note(db_session, user_id=a_user.id)
    entry_1: ClientReportNoteRead = (  # noqa: F841
        await create_random_client_report_note(
            db_session, client_report_id=a_report.id, note_id=note_1.id
        )
    )
    entry_2: ClientReportNoteRead = (  # noqa: F841
        await create_random_client_report_note(
            db_session, client_report_id=a_report.id, note_id=note_2.id
        )
    )
    entry_3: ClientReportNoteRead = (  # noqa: F841
        await create_random_client_report_note(
            db_session, client_report_id=a_report.id, note_id=note_3.id
        )
    )
    entry_4: ClientReportNoteRead = (  # noqa: F841
        await create_random_client_report_note(
            db_session, client_report_id=a_report.id, note_id=note_4.id
        )
    )
    response: Response = await client.get(
        f"clients/reports/{a_client.id}/{a_report.id}/notes",
        headers=admin_token_headers,
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    assert data["page"] == 1
    assert data["total"] == 4
    assert data["size"] == 1000
    assert len(data["results"]) == 4
    for entry in data["results"]:
        if entry["id"] == str(note_1.id):
            assert entry["title"] == note_1.title
            assert entry["description"] == note_1.description
            assert entry["is_active"] == note_1.is_active
            assert entry["user_id"] == str(a_user.id)
        if entry["id"] == str(note_2.id):
            assert entry["title"] == note_2.title
            assert entry["description"] == note_2.description
            assert entry["is_active"] == note_2.is_active
            assert entry["user_id"] == str(a_user.id)
        if entry["id"] == str(note_3.id):
            assert entry["title"] == note_3.title
            assert entry["description"] == note_3.description
            assert entry["is_active"] == note_3.is_active
            assert entry["user_id"] == str(a_user.id)
        if entry["id"] == str(note_4.id):
            assert entry["title"] == note_4.title
            assert entry["description"] == note_4.description
            assert entry["is_active"] == note_4.is_active
            assert entry["user_id"] == str(a_user.id)


async def test_list_all_client_report_notes_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    b_user: User = await get_user_by_email(db_session, settings.auth.first_admin)
    a_client: ClientRead = await create_random_client(db_session)
    a_user_a_client: UserClient = await assign_user_to_client(
        db_session, a_user, a_client
    )
    a_report: ClientReportRead = await create_random_client_report(
        db_session, client_id=a_user_a_client.client_id
    )
    note_1: NoteRead = await create_random_note(db_session, user_id=a_user.id)
    note_2: NoteRead = await create_random_note(db_session, user_id=a_user.id)
    note_3: NoteRead = await create_random_note(db_session, user_id=b_user.id)
    note_4: NoteRead = await create_random_note(db_session, user_id=b_user.id)
    entry_1: ClientReportNoteRead = (  # noqa: F841
        await create_random_client_report_note(
            db_session, client_report_id=a_report.id, note_id=note_1.id
        )
    )
    entry_2: ClientReportNoteRead = (  # noqa: F841
        await create_random_client_report_note(
            db_session, client_report_id=a_report.id, note_id=note_2.id
        )
    )
    entry_3: ClientReportNoteRead = (  # noqa: F841
        await create_random_client_report_note(
            db_session, client_report_id=a_report.id, note_id=note_3.id
        )
    )
    entry_4: ClientReportNoteRead = (  # noqa: F841
        await create_random_client_report_note(
            db_session, client_report_id=a_report.id, note_id=note_4.id
        )
    )
    response: Response = await client.get(
        f"clients/reports/{a_client.id}/{a_report.id}/notes",
        headers=employee_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == 4
    assert data["size"] == 1000
    assert len(data["results"]) == 4
    for entry in data["results"]:
        if entry["id"] == str(note_1.id):
            assert entry["title"] == note_1.title
            assert entry["description"] == note_1.description
            assert entry["is_active"] == note_1.is_active
            assert entry["user_id"] == str(a_user.id)
        if entry["id"] == str(note_2.id):
            assert entry["title"] == note_2.title
            assert entry["description"] == note_2.description
            assert entry["is_active"] == note_2.is_active
            assert entry["user_id"] == str(a_user.id)
        if entry["id"] == str(note_3.id):
            assert entry["title"] == note_3.title
            assert entry["description"] == note_3.description
            assert entry["is_active"] == note_3.is_active
            assert entry["user_id"] == str(b_user.id)
        if entry["id"] == str(note_4.id):
            assert entry["title"] == note_4.title
            assert entry["description"] == note_4.description
            assert entry["is_active"] == note_4.is_active
            assert entry["user_id"] == str(b_user.id)
