from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string
from tests.utils.website_maps import create_random_website_map
from tests.utils.websites import create_random_website

from app.api.exceptions import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.schemas import WebsiteMapRead, WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_create_website_sitemap_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    website: WebsiteRead = await create_random_website(db_session)
    data = {
        "url": "/sitemap_index.xml",
        "website_id": str(website.id),
    }
    response: Response = await client.post(
        "sitemaps/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["id"] is not None
    assert entry["url"] == data["url"]
    assert entry["website_id"] == str(website.id)


async def test_create_website_sitemap_as_superuser_url_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    data = {
        "url": sitemap.url,
        "website_id": str(sitemap.website_id),
    }
    response: Response = await client.post(
        "sitemaps/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    entry: Dict[str, Any] = response.json()
    assert entry["detail"] == ErrorCode.WEBSITE_MAP_EXISTS


async def test_create_website_sitemap_as_superuser_unassigned_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    fake_id: str = get_uuid_str()
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    data = {
        "url": sitemap.url,
        "website_id": fake_id,
    }
    response: Response = await client.post(
        "sitemaps/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    entry: Dict[str, Any] = response.json()
    assert entry["detail"] == ErrorCode.WEBSITE_NOT_FOUND


async def test_create_website_sitemap_as_superuser_url_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    data = {
        "url": "",
        "website_id": str(sitemap.website_id),
    }
    response: Response = await client.post(
        "sitemaps/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "Value error, url must be 1 characters or more"


async def test_create_website_sitemap_as_superuser_url_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    long_url: str = random_lower_string(chars=5001)
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    data = {
        "url": long_url,
        "website_id": str(sitemap.website_id),
    }
    response: Response = await client.post(
        "sitemaps/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"] == "Value error, url must be 2048 characters or less"
    )
