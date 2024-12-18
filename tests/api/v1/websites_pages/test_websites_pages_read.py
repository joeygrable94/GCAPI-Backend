from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_pages import create_random_website_page

from app.api.exceptions import ErrorCode
from app.core.utilities import get_uuid_str
from app.crud import WebsitePageRepository
from app.schemas import WebsitePageRead

pytestmark = pytest.mark.asyncio


async def test_read_website_page_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_page: WebsitePageRead = await create_random_website_page(db_session)
    response: Response = await client.get(
        f"webpages/{website_page.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(website_page.id)
    assert data["url"] == website_page.url
    repo: WebsitePageRepository = WebsitePageRepository(db_session)
    existing_data: Any = await repo.exists_by_fields(
        {
            "url": website_page.url,
            "website_id": website_page.website_id,
        }
    )
    assert existing_data
    assert existing_data.url == data["url"]


async def test_read_website_page_by_id_as_superuser_page_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"webpages/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.WEBSITE_PAGE_NOT_FOUND
