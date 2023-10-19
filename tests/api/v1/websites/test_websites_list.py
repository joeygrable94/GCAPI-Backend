from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.websites import create_random_website

from app.schemas import WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_list_websites_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_1: WebsiteRead = await create_random_website(db_session)
    response: Response = await client.get("websites/", headers=superuser_token_headers)
    assert 200 <= response.status_code < 300
    all_entries: Any = response.json()
    assert len(all_entries) >= 1
    for entry in all_entries:
        assert "domain" in entry
        assert "is_secure" in entry
        if entry["domain"] == entry_1.domain:
            assert entry["domain"] == entry_1.domain
            assert isinstance(entry["is_secure"], bool)
