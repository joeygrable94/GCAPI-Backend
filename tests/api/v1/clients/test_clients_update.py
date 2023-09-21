from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.utils import random_lower_string

from app.api.errors import ErrorCode
from app.schemas import ClientRead, ClientUpdate

pytestmark = pytest.mark.asyncio


async def test_update_client_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: ClientRead = await create_random_client(db_session)
    title: str = "New Client Title"
    data: Dict[str, str] = {"title": title}
    response: Response = await client.patch(
        f"clients/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert updated_entry["title"] == title
    assert updated_entry["id"] == str(entry_a.id)
    assert updated_entry["description"] == entry_a.description


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
    assert updated_entry["detail"][0]["msg"] == "Value error, title must be 5 characters or more"


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
    assert updated_entry["detail"][0]["msg"] == "Value error, title must be 96 characters or less"


async def test_update_client_as_superuser_description_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: ClientRead = await create_random_client(db_session)
    description: str = random_lower_string() * 160
    data: Dict[str, str] = {"description": description}
    response: Response = await client.patch(
        f"clients/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == "Value error, description must be 5000 characters or less"
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
        description="New description",
    )
    response: Response = await client.patch(
        f"clients/{entry_a.id}",
        headers=superuser_token_headers,
        json=update_dict.model_dump(),
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_entry["detail"] == ErrorCode.CLIENT_EXISTS
