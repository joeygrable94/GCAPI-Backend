from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string
from tests.utils.website_maps import create_random_website_map
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

from app.api.exceptions import ErrorCode
from app.core.utilities.uuids import get_uuid
from app.schemas import WebsiteMapRead, WebsitePageRead, WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_create_website_page_as_superuser(
    celery_worker: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    website: WebsiteRead = await create_random_website(db_session)
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    data = {
        "url": "/",
        "status": 200,
        "priority": 0.5,
        "website_id": str(website.id),
        "sitemap_id": str(sitemap.id),
    }
    response: Response = await client.post(
        "webpages/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["url"] == "/"
    assert entry["status"] == 200
    assert entry["priority"] == 0.5
    assert entry["website_id"] == str(website.id)
    assert entry["sitemap_id"] == str(sitemap.id)


async def test_create_website_page_as_superuser_url_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    webpage: WebsitePageRead = await create_random_website_page(db_session)
    data = {
        "url": webpage.url,
        "status": 200,
        "priority": 0.5,
        "website_id": str(webpage.website_id),
        "sitemap_id": str(webpage.sitemap_id),
    }
    response: Response = await client.post(
        "webpages/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    entry: Dict[str, Any] = response.json()
    assert entry["detail"] == ErrorCode.WEBSITE_PAGE_URL_EXISTS


async def test_create_website_page_as_superuser_url_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    webpage: WebsitePageRead = await create_random_website_page(db_session)
    data = {
        "url": "",
        "status": 200,
        "priority": 0.5,
        "website_id": str(webpage.website_id),
        "sitemap_id": str(webpage.sitemap_id),
    }
    response: Response = await client.post(
        "webpages/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "Value error, url must be 1 characters or more"


async def test_create_website_page_as_superuser_url_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    long_url: str = random_lower_string(chars=5001)
    webpage: WebsitePageRead = await create_random_website_page(db_session)
    data = {
        "url": long_url,
        "status": 200,
        "priority": 0.5,
        "website_id": str(webpage.website_id),
        "sitemap_id": str(webpage.sitemap_id),
    }
    response: Response = await client.post(
        "webpages/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"] == "Value error, url must be 2048 characters or less"
    )


async def test_create_website_page_as_superuser_website_not_exists(
    celery_worker: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    website: WebsiteRead = await create_random_website(db_session)  # noqa: F841
    web_fake_id: UUID4 = get_uuid()
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    data = {
        "url": "/",
        "status": 200,
        "priority": 0.5,
        "website_id": str(web_fake_id),
        "sitemap_id": str(sitemap.id),
    }
    response: Response = await client.post(
        "webpages/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    entry: Dict[str, Any] = response.json()
    assert entry["detail"] == ErrorCode.WEBSITE_NOT_FOUND
