from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string
from tests.utils.website_pages import create_random_website_page

from app.schemas import WebsitePageRead

pytestmark = pytest.mark.asyncio


async def test_update_website_page(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: WebsitePageRead = await create_random_website_page(db_session)
    response: Response = await client.patch(
        f"webpages/{entry_a.id}",
        headers=superuser_token_headers,
        json={
            "url": "/",
            "status": 301,
            "priority": 0.1,
        },
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["id"] == str(entry_a.id)
    assert entry["url"] == "/"
    assert entry["status"] == 301
    assert entry["priority"] == 0.1
    assert entry["website_id"] == str(entry_a.website_id)
    assert entry["sitemap_id"] == str(entry_a.sitemap_id)


async def test_update_website_page_as_superuser_url_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    long_url: str = random_lower_string(chars=5001)
    entry_a: WebsitePageRead = await create_random_website_page(db_session)
    response: Response = await client.patch(
        f"webpages/{entry_a.id}",
        headers=superuser_token_headers,
        json={
            "url": long_url,
            "status": 301,
        },
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "url must contain less than 5000 characters"
