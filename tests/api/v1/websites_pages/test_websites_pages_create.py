from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string
from tests.utils.website_maps import create_random_website_map
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

from app.api.errors import ErrorCode
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
    assert entry["page"] is not None
    assert entry["mobile_task_id"] is not None
    assert entry["desktop_task_id"] is not None
    web_page = entry["page"]
    assert web_page["url"] == "/"
    assert web_page["status"] == 200
    assert web_page["priority"] == 0.5
    assert web_page["website_id"] == str(website.id)
    assert web_page["sitemap_id"] == str(sitemap.id)
    mobile_task_id = entry["mobile_task_id"]
    m_response: Response = await client.get(
        f"tasks/{mobile_task_id}",
        headers=superuser_token_headers,
    )
    assert m_response.status_code == 200
    m_content = m_response.json()
    assert m_content == {
        "task_id": str(mobile_task_id),
        "task_status": "PENDING",
        "task_result": None,
    }
    desktop_task_id = entry["desktop_task_id"]
    d_response: Response = await client.get(
        f"tasks/{desktop_task_id}",
        headers=superuser_token_headers,
    )
    assert d_response.status_code == 200
    d_content = d_response.json()
    assert d_content == {
        "task_id": str(desktop_task_id),
        "task_status": "PENDING",
        "task_result": None,
    }


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
    assert entry["detail"][0]["msg"] == "url text is required"


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
    assert entry["detail"][0]["msg"] == "url must contain less than 5000 characters"
