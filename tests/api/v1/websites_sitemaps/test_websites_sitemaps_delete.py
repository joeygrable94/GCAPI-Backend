from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_maps import create_random_website_map

from app.api.exceptions import ErrorCode
from app.schemas import WebsiteMapRead

pytestmark = pytest.mark.asyncio


async def test_delete_website_sitemap_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry: WebsiteMapRead = await create_random_website_map(db_session)
    response: Response = await client.delete(
        f"sitemaps/{entry.id}",
        headers=admin_token_headers,
    )
    assert 200 <= response.status_code < 300
    response: Response = await client.get(
        f"sitemaps/{entry.id}",
        headers=admin_token_headers,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.WEBSITE_MAP_NOT_FOUND
