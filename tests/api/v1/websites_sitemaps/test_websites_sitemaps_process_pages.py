import unittest.mock
from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_maps import create_random_website_map

from app.api.exceptions.errors import ErrorCode
from app.schemas import WebsiteMapRead

pytestmark = pytest.mark.asyncio


async def test_sitemap_process_sitemap_pages_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    # mock is_sitemap_url_xml_valid
    with unittest.mock.patch(
        "app.crud.website_map.WebsiteMapRepository.is_sitemap_url_xml_valid"
    ) as mock_valid_sitemap_xml:
        mock_valid_sitemap_xml.return_value = True
        response: Response = await client.get(
            f"sitemaps/{a_sitemap.id}/process-pages",
            headers=admin_token_headers,
        )
        data: Dict[str, Any] = response.json()
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
    admin_token_headers: Dict[str, str],
) -> None:
    a_sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    # mock fetch_url_status_code
    with unittest.mock.patch(
        "app.core.utilities.websites.fetch_url_status_code"
    ) as mock_fetch_url_status_code:
        mock_fetch_url_status_code.return_value = 404
        response: Response = await client.get(
            f"sitemaps/{a_sitemap.id}/process-pages",
            headers=admin_token_headers,
        )
        assert response.status_code == 400
        entry: Dict[str, Any] = response.json()
        assert entry["detail"] == ErrorCode.WEBSITE_MAP_URL_XML_INVALID


async def test_sitemap_process_sitemap_pages_as_superuser_url_xml_invalid(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    # mock check_is_xml_valid_sitemap
    with unittest.mock.patch(
        "app.core.utilities.websites.check_is_xml_valid_sitemap"
    ) as mock_check_is_xml_valid_sitemap:
        mock_check_is_xml_valid_sitemap.return_value = False
        response: Response = await client.get(
            f"sitemaps/{a_sitemap.id}/process-pages",
            headers=admin_token_headers,
        )
        assert response.status_code == 400
        entry: Dict[str, Any] = response.json()
        assert entry["detail"] == ErrorCode.WEBSITE_MAP_URL_XML_INVALID
