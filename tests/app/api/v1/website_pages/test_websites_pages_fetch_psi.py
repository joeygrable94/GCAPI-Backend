from typing import Any

import pytest
from httpx import AsyncClient, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import ErrorCode
from app.core.utilities import get_uuid
from app.schemas import WebsiteMapRead, WebsitePageRead
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.website_maps import create_random_website_map
from tests.utils.website_pages import create_random_website_page

pytestmark = pytest.mark.asyncio


async def test_fetch_website_page_speed_insights_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    entry: WebsitePageRead = await create_random_website_page(db_session)
    response: Response = await client.post(
        f"webpages/{entry.id}/process-psi", headers=admin_user.token_headers
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 200
    assert data["id"] == str(entry.id)
    assert data["is_active"] == entry.is_active
    assert data["url"] == entry.url
    assert data["status"] == entry.status
    assert data["priority"] == entry.priority
    assert data["website_id"] == str(entry.website_id)
    assert data["sitemap_id"] == str(entry.sitemap_id)


async def test_fetch_website_page_psi_by_id_as_superuser_website_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    web_fake_id: UUID4 = get_uuid()
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    entry: WebsitePageRead = await create_random_website_page(
        db_session,
        website_id=web_fake_id,
        sitemap_id=sitemap.id,
    )
    response: Response = await client.post(
        f"webpages/{entry.id}/process-psi", headers=admin_user.token_headers
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ErrorCode.ENTITY_NOT_FOUND in data["detail"]
