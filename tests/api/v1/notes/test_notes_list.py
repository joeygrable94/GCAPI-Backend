from typing import Any
from typing import Dict

import pytest
from httpx import AsyncClient
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.notes import create_random_note
from tests.utils.users import get_user_by_email

from app.core.config import settings
from app.models import User
from app.schemas import NoteRead

pytestmark = pytest.mark.asyncio


async def test_list_notess_as_superuser(
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
    all_entries: Any = response.json()
    assert len(all_entries) > 1
    for entry in all_entries:
        assert "title" in entry
        assert "description" in entry
        assert "is_active" in entry
        assert "user_id" in entry
        assert entry["user_id"] == str(user.id)
        if entry["title"] == entry_1.title:
            assert entry["title"] == entry_1.title
            assert entry["description"] == entry_1.description
        if entry["title"] == entry_2.title:
            assert entry["title"] == entry_2.title
            assert entry["description"] == entry_2.description
        if entry["title"] == entry_3.title:
            assert entry["title"] == entry_3.title
            assert entry["description"] == entry_3.description
        if entry["title"] == entry_4.title:
            assert entry["title"] == entry_4.title
            assert entry["description"] == entry_4.description
