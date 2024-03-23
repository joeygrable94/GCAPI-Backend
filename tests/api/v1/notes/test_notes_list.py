from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.notes import create_random_note
from tests.utils.users import get_user_by_email

from app.core.config import settings
from app.models import User
from app.schemas import NoteRead

pytestmark = pytest.mark.asyncio


async def test_list_all_notes_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_admin
    )
    entry_1: NoteRead = await create_random_note(db_session, user_id=user.id)
    entry_2: NoteRead = await create_random_note(db_session, user_id=user.id)
    entry_3: NoteRead = await create_random_note(db_session, user_id=user.id)
    entry_4: NoteRead = await create_random_note(db_session, user_id=user.id)
    response: Response = await client.get("notes/", headers=admin_token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 4
    assert data["size"] == 1000
    assert len(data["results"]) == 4
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["title"] == entry_1.title
            assert entry["description"] == entry_1.description
            assert entry["is_active"] == entry_1.is_active
            assert entry["user_id"] == str(entry_1.user_id)
        if entry["id"] == str(entry_2.id):
            assert entry["title"] == entry_2.title
            assert entry["description"] == entry_2.description
            assert entry["is_active"] == entry_2.is_active
            assert entry["user_id"] == str(entry_2.user_id)
        if entry["id"] == str(entry_3.id):
            assert entry["title"] == entry_3.title
            assert entry["description"] == entry_3.description
            assert entry["is_active"] == entry_3.is_active
            assert entry["user_id"] == str(entry_3.user_id)
        if entry["id"] == str(entry_4.id):
            assert entry["title"] == entry_4.title
            assert entry["description"] == entry_4.description
            assert entry["is_active"] == entry_4.is_active
            assert entry["user_id"] == str(entry_4.user_id)


async def test_list_all_notes_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_employee
    )
    entry_1: NoteRead = await create_random_note(db_session, user_id=user.id)
    entry_2: NoteRead = await create_random_note(db_session, user_id=user.id)
    response: Response = await client.get("notes/", headers=employee_token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 2
    assert data["size"] == 1000
    assert len(data["results"]) == 2
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["title"] == entry_1.title
            assert entry["description"] == entry_1.description
            assert entry["is_active"] == entry_1.is_active
            assert entry["user_id"] == str(entry_1.user_id)
        if entry["id"] == str(entry_2.id):
            assert entry["title"] == entry_2.title
            assert entry["description"] == entry_2.description
            assert entry["is_active"] == entry_2.is_active
            assert entry["user_id"] == str(entry_2.user_id)
