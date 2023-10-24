from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_maps import create_random_website_map

from app.api.exceptions import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.crud import WebsiteMapRepository
from app.schemas import WebsiteMapRead

pytestmark = pytest.mark.asyncio


async def test_read_website_sitemaps_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    response: Response = await client.get(
        f"sitemaps/{sitemap.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(sitemap.id)
    assert data["url"] == sitemap.url
    repo: WebsiteMapRepository = WebsiteMapRepository(db_session)
    existing_data: Any = await repo.exists_by_two(
        field_name_a="url",
        field_value_a=sitemap.url,
        field_name_b="website_id",
        field_value_b=sitemap.website_id,
    )
    assert existing_data
    assert existing_data.url == data["url"]


async def test_read_website_sitemaps_by_id_as_superuser_page_not_found(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"sitemaps/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.WEBSITE_MAP_NOT_FOUND
