from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.notes import create_random_note
from tests.utils.users import get_user_by_email

from app.api.exceptions.errors import ErrorCode
from app.core.config import settings
from app.core.utilities.uuids import get_uuid_str
from app.crud import NoteRepository
from app.models import Note, User
from app.schemas import NoteRead

pytestmark = pytest.mark.asyncio


async def test_read_note_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_admin
    )
    entry: NoteRead = await create_random_note(db_session, user_id=user.id)
    response: Response = await client.get(
        f"notes/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    assert "title" in data
    assert "description" in data
    assert data["is_active"] is True
    assert data["user_id"] == str(user.id)
    repo: NoteRepository = NoteRepository(db_session)
    existing_data: Note | None = await repo.read_by("title", entry.title)
    assert existing_data
    assert existing_data.title == data["title"]
    assert existing_data.description == data["description"]
    assert str(existing_data.user_id) == data["user_id"]
    assert existing_data.is_active == data["is_active"]


async def test_read_note_by_id_as_superuser_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"notes/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.NOTE_NOT_FOUND
