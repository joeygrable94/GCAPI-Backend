from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.errors import ErrorCode
from tests.utils.clients import create_random_client
from tests.utils.utils import random_lower_string

from app.schemas import ClientRead, ClientUpdate

pytestmark = pytest.mark.asyncio


async def test_update_client_as_superuser_title_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: ClientRead = await create_random_client(db_session)
    title: str = "1234"
    data: Dict[str, str] = {"title": title}
    response: Response = await client.patch(
        f"clients/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"] == "title must contain 5 or more characters"
    )


async def test_update_client_as_superuser_title_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: ClientRead = await create_random_client(db_session)
    title: str = random_lower_string() * 4
    data: Dict[str, str] = {"title": title}
    response: Response = await client.patch(
        f"clients/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == "title must contain less than 96 characters"
    )


async def test_update_client_as_superuser_content_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: ClientRead = await create_random_client(db_session)
    content: str = random_lower_string() * 10
    data: Dict[str, str] = {"content": content}
    response: Response = await client.patch(
        f"clients/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == "content must contain less than 255 characters"
    )


async def test_update_client_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: ClientRead = await create_random_client(db_session)
    entry_b: ClientRead = await create_random_client(db_session)
    update_dict = ClientUpdate(
        title=entry_b.title,
        content="New Content",
    )
    response: Response = await client.patch(
        f"clients/{entry_a.id}",
        headers=superuser_token_headers,
        json=update_dict.dict(),
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_entry["detail"] == ErrorCode.CLIENT_EXISTS
