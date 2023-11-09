from typing import Any
from typing import Dict

import pytest
from httpx import AsyncClient
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_maps import create_random_website_map

from app.schemas import WebsiteMapRead

pytestmark = pytest.mark.asyncio


async def test_sitemap_process_sitemap_pages_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry: WebsiteMapRead = await create_random_website_map(db_session)
    response: Response = await client.get(
        f"sitemaps/{entry.id}/process-pages",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert "url" in data
    assert "website_id" in data
    assert "task_id" in data
