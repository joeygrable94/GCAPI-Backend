import unittest.mock
from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.schemas import WebsiteMapRead
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.website_maps import create_random_website_map
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


async def test_sitemap_process_sitemap_pages_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    # mock is_sitemap_url_xml_valid
    with unittest.mock.patch(
        "app.crud.website_map.WebsiteMapRepository.is_sitemap_url_xml_valid"
    ) as mock_valid_sitemap_xml:
        mock_valid_sitemap_xml.return_value = True
        response: Response = await client.get(
            f"sitemaps/{a_sitemap.id}/process-pages",
            headers=admin_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 200
        assert "url" in data
        assert "website_id" in data
        assert "sitemap_id" in data
        assert data["url"] == a_sitemap.url
        assert data["website_id"] == str(a_sitemap.website_id)
        assert data["sitemap_id"] == str(a_sitemap.id)


async def test_sitemap_process_sitemap_pages_as_superuser_xml_url_status_code_error(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session, domain="getcommunity.com")
    a_sitemap = await create_random_website_map(
        db_session, url_path="sitemap-invalid.xml", website_id=a_website.id
    )
    with unittest.mock.patch(
        "app.core.utilities.websites.fetch_url_status_code"
    ) as mock_fetch_url_status_code:
        mock_fetch_url_status_code.return_value = 404
        response: Response = await client.get(
            f"sitemaps/{a_sitemap.id}/process-pages",
            headers=admin_user.token_headers,
        )
        assert response.status_code == 422
        entry: dict[str, Any] = response.json()
        assert entry["detail"] == ErrorCode.XML_INVALID


async def test_update_website_sitemap_as_superuser_url_invalid_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    bad_website_id = get_uuid_str()
    a_sitemap = await create_random_website_map(
        db_session, website_id=bad_website_id, url_path="sitemap.xml"
    )
    with unittest.mock.patch(
        "app.core.utilities.websites.check_is_xml_valid_sitemap"
    ) as mock_check_is_xml_valid_sitemap:
        mock_check_is_xml_valid_sitemap.return_value = False
        response: Response = await client.get(
            f"sitemaps/{a_sitemap.id}/process-pages",
            headers=admin_user.token_headers,
        )
        assert response.status_code == 404
        entry: dict[str, Any] = response.json()
        assert ErrorCode.ENTITY_NOT_FOUND in entry["detail"]
