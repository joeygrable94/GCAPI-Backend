from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.websites import create_random_website

from app.schemas import WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_list_all_websites_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_1: WebsiteRead = await create_random_website(db_session)
    response: Response = await client.get("websites/", headers=admin_token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 13
    assert data["size"] == 100
    assert len(data["results"]) == 13
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["domain"] == entry_1.domain
            assert entry["is_secure"] == entry_1.is_secure
