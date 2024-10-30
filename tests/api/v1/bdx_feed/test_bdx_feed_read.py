from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.bdx_feed import create_random_bdx_feed
from tests.utils.clients import create_random_client

from app.api.exceptions.errors import ErrorCode
from app.core.utilities import get_uuid_str
from app.crud import BdxFeedRepository
from app.models import BdxFeed
from app.schemas import BdxFeedRead, ClientRead

pytestmark = pytest.mark.asyncio


async def test_read_bdx_feed_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry: BdxFeedRead = await create_random_bdx_feed(db_session, client_id=a_client.id)
    response: Response = await client.get(
        f"bdx/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    assert "username" in data
    assert "password" in data
    assert "serverhost" in data
    assert data["client_id"] == str(a_client.id)
    repo: BdxFeedRepository = BdxFeedRepository(db_session)
    existing_data: BdxFeed | None = await repo.read(entry.id)
    assert existing_data
    assert existing_data.username == data["username"]
    assert existing_data.password == data["password"]
    assert existing_data.serverhost == data["serverhost"]
    assert str(existing_data.client_id) == data["client_id"]


async def test_read_bdx_feed_by_id_as_superuser_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"bdx/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.BDX_FEED_NOT_FOUND
