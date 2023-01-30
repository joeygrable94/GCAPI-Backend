from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client

from app.api.errors import ErrorCode
from app.db.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_list_clients_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_1: ClientRead = await create_random_client(db_session)
    entry_2: ClientRead = await create_random_client(db_session)
    response: Response = await client.get("clients/", headers=superuser_token_headers)
    assert 200 <= response.status_code < 300
    all_entries: Any = response.json()
    assert len(all_entries) > 1
    for entry in all_entries:
        assert "title" in entry
        assert "content" in entry
        if entry["title"] == entry_1.title:
            assert entry["title"] == entry_1.title
            assert entry["content"] == entry_1.content
        if entry["title"] == entry_2.title:
            assert entry["title"] == entry_2.title
            assert entry["content"] == entry_2.content


async def test_list_clients_as_testuser(
    client: AsyncClient,
    db_session: AsyncSession,
    testuser_token_headers: Dict[str, str],
) -> None:
    entry_1: ClientRead = await create_random_client(db_session)  # noqa: F841
    entry_2: ClientRead = await create_random_client(db_session)  # noqa: F841
    response: Response = await client.get("clients/", headers=testuser_token_headers)
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS
