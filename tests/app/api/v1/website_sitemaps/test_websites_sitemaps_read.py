from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import ErrorCode
from app.core.utilities import get_uuid_str
from app.crud import WebsiteMapRepository
from app.schemas import WebsiteMapRead
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.website_maps import create_random_website_map

pytestmark = pytest.mark.asyncio


async def test_read_website_sitemaps_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    response: Response = await client.get(
        f"sitemaps/{sitemap.id}",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(sitemap.id)
    assert data["url"] == sitemap.url
    repo: WebsiteMapRepository = WebsiteMapRepository(db_session)
    existing_data: Any = await repo.exists_by_fields(
        {
            "url": sitemap.url,
            "website_id": sitemap.website_id,
        }
    )
    assert existing_data
    assert existing_data.url == data["url"]


async def test_read_website_sitemaps_by_id_as_superuser_page_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"sitemaps/{entry_id}",
        headers=admin_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ErrorCode.ENTITY_NOT_FOUND in data["detail"]
