from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string
from tests.utils.website_maps import create_random_website_map

from app.schemas import WebsiteMapRead

pytestmark = pytest.mark.asyncio


async def test_update_website_sitemaps(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    data = {
        "url": "/new-sitemap.xml",
    }
    response: Response = await client.patch(
        f"sitemaps/{sitemap.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["id"] == str(sitemap.id)
    assert entry["url"] == "/new-sitemap.xml"
    assert entry["website_id"] == str(sitemap.website_id)


async def test_update_website_sitemaps_as_superuser_url_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    long_url: str = random_lower_string(chars=5001)
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    response: Response = await client.patch(
        f"sitemaps/{sitemap.id}",
        headers=superuser_token_headers,
        json={
            "url": long_url,
        },
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "url must be 2048 characters or less"
