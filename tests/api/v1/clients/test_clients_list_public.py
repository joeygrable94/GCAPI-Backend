from typing import Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client

from app.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_list_public_clients_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_1: ClientRead = await create_random_client(db_session)
    entry_2: ClientRead = await create_random_client(  # noqa: F841
        db_session, is_active=False
    )
    entry_3: ClientRead = await create_random_client(db_session)
    response: Response = await client.get("clients/public", headers=admin_token_headers)
    assert 200 <= response.status_code < 300
    data = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == 4
    assert data["size"] == 1000
    assert len(data["results"]) == 4
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["title"] == entry_1.title
            assert "slug" not in entry
            assert "description" not in entry
            assert "is_active" not in entry
            assert "style_guide" in entry
        if entry["id"] == str(entry_3.id):
            assert entry["title"] == entry_3.title
            assert "slug" not in entry
            assert "description" not in entry
            assert "is_active" not in entry
            assert "style_guide" in entry


async def test_list_public_clients_as_verified_user(
    client: AsyncClient,
    db_session: AsyncSession,
    user_verified_token_headers: Dict[str, str],
) -> None:
    entry_1: ClientRead = await create_random_client(db_session)
    entry_2: ClientRead = await create_random_client(  # noqa: F841
        db_session, is_active=False
    )
    entry_3: ClientRead = await create_random_client(db_session)
    response: Response = await client.get(
        "clients/public", headers=user_verified_token_headers
    )
    assert 200 <= response.status_code < 300
    data = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == 4
    assert data["size"] == 1000
    assert len(data["results"]) == 4
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["title"] == entry_1.title
            assert "slug" not in entry
            assert "description" not in entry
            assert "is_active" not in entry
            assert "style_guide" in entry
        if entry["id"] == str(entry_3.id):
            assert entry["title"] == entry_3.title
            assert "slug" not in entry
            assert "description" not in entry
            assert "is_active" not in entry
            assert "style_guide" in entry
