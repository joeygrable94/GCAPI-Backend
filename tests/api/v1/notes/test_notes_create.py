from typing import Any
from typing import Dict

import pytest
from httpx import AsyncClient
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.models.user import User

pytestmark = pytest.mark.asyncio


async def test_create_note_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_admin
    )
    title: str = random_lower_string()
    description: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "title": title,
        "description": description,
        "user_id": str(user.id),
    }
    response: Response = await client.post(
        "notes/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == title
    assert entry["description"] == description
    assert entry["is_active"] is True


async def test_create_note_as_superuser_note_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_admin
    )
    title: str = random_lower_string()
    description: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "title": title,
        "description": description,
        "user_id": str(user.id),
    }
    response: Response = await client.post(
        "notes/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["title"] == title
    assert entry["description"] == description
    assert entry["is_active"] is True
    description_2: str = random_lower_string()
    data_in_2: Dict[str, Any] = {
        "title": title,
        "description": description_2,
        "user_id": str(
            user.id,
        ),
    }
    response_2: Response = await client.post(
        "notes/",
        headers=admin_token_headers,
        json=data_in_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ErrorCode.NOTE_EXISTS


async def test_create_note_as_superuser_note_title_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_admin
    )
    title: str = "1234"
    description: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "title": title,
        "description": description,
        "user_id": str(user.id),
    }
    response: Response = await client.post(
        "notes/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"] == "Value error, title must be 5 characters or more"
    )


async def test_create_note_as_superuser_note_title_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_admin
    )
    title: str = random_lower_string() * 4
    description: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "title": title,
        "description": description,
        "user_id": str(user.id),
    }
    response: Response = await client.post(
        "notes/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"] == "Value error, title must be 96 characters or less"
    )


async def test_create_note_as_superuser_note_description_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_admin
    )
    title: str = random_lower_string()
    description: str = random_lower_string() * 160
    data_in: Dict[str, Any] = {
        "title": title,
        "description": description,
        "user_id": str(user.id),
    }
    response: Response = await client.post(
        "notes/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == "Value error, description must be 5000 characters or less"
    )  # noqa: E501
