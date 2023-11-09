from typing import Any
from typing import Dict

import pytest
from httpx import AsyncClient
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.notes import create_random_note
from tests.utils.users import get_user_by_email

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.models import User
from app.schemas import NoteRead

pytestmark = pytest.mark.asyncio


async def test_delete_note_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_admin
    )
    entry: NoteRead = await create_random_note(db_session, user_id=user.id)
    response: Response = await client.delete(
        f"notes/{entry.id}",
        headers=admin_token_headers,
    )
    assert 200 <= response.status_code < 300
    response: Response = await client.get(
        f"notes/{entry.id}",
        headers=admin_token_headers,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.NOTE_NOT_FOUND
