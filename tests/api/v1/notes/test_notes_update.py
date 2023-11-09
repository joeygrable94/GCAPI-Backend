from typing import Any
from typing import Dict

import pytest
from httpx import AsyncClient
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.notes import create_random_note
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.models import User
from app.schemas import NoteRead
from app.schemas import NoteUpdate

pytestmark = pytest.mark.asyncio


async def test_update_note_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_admin
    )
    entry_a: NoteRead = await create_random_note(db_session, user_id=user.id)
    title: str = "New Client Title"
    data: Dict[str, str] = {"title": title}
    response: Response = await client.patch(
        f"notes/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert updated_entry["title"] == title
    assert updated_entry["id"] == str(entry_a.id)
    assert updated_entry["description"] == entry_a.description


async def test_update_note_as_superuser_title_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_admin
    )
    entry_a: NoteRead = await create_random_note(db_session, user_id=user.id)
    title: str = "1234"
    data: Dict[str, str] = {"title": title}
    response: Response = await client.patch(
        f"notes/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == "Value error, title must be 5 characters or more"
    )


async def test_update_note_as_superuser_title_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_admin
    )
    entry_a: NoteRead = await create_random_note(db_session, user_id=user.id)
    title: str = random_lower_string() * 4
    data: Dict[str, str] = {"title": title}
    response: Response = await client.patch(
        f"notes/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == "Value error, title must be 96 characters or less"
    )


async def test_update_note_as_superuser_description_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_admin
    )
    entry_a: NoteRead = await create_random_note(db_session, user_id=user.id)
    description: str = random_lower_string() * 160
    data: Dict[str, str] = {"description": description}
    response: Response = await client.patch(
        f"notes/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == "Value error, description must be 5000 characters or less"
    )


async def test_update_note_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_admin
    )
    entry_a: NoteRead = await create_random_note(db_session, user_id=user.id)
    entry_b: NoteRead = await create_random_note(db_session, user_id=user.id)
    update_dict = NoteUpdate(
        title=entry_b.title,
        description="New description",
    )
    response: Response = await client.patch(
        f"notes/{entry_a.id}",
        headers=admin_token_headers,
        json=update_dict.model_dump(),
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_entry["detail"] == ErrorCode.NOTE_EXISTS
