import unittest.mock
from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import ERROR_MESSAGE_ENTITY_NOT_FOUND
from app.entities.website_sitemap.constants import ERROR_MESSAGE_XML_INVALID
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.website_maps import create_random_website_map
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


async def test_sitemap_process_sitemap_pages_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(
        db_session, domain="getcommunity.com", is_secure=True
    )
    a_sitemap = await create_random_website_map(db_session, a_website.id, "sitemap.xml")
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
        "app.entities.website_page.utilities.fetch_url_status_code"
    ) as mock_fetch_url_status_code:
        mock_fetch_url_status_code.return_value = 404
        response: Response = await client.get(
            f"sitemaps/{a_sitemap.id}/process-pages",
            headers=admin_user.token_headers,
        )
        assert response.status_code == 422
        entry: dict[str, Any] = response.json()
        assert entry["detail"] == ERROR_MESSAGE_XML_INVALID


async def test_update_website_sitemap_as_superuser_url_invalid_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    bad_website_id = get_uuid_str()
    a_sitemap = await create_random_website_map(
        db_session, website_id=bad_website_id, url_path="sitemap.xml"
    )
    # "app.utilities.websites.check_is_xml_valid_sitemap"
    with unittest.mock.patch(
        "app.entities.website_sitemap.utilities.check_is_xml_valid_sitemap"
    ) as mock_check_is_xml_valid_sitemap:
        mock_check_is_xml_valid_sitemap.return_value = False
        response: Response = await client.get(
            f"sitemaps/{a_sitemap.id}/process-pages",
            headers=admin_user.token_headers,
        )
        assert response.status_code == 404
        entry: dict[str, Any] = response.json()
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in entry["detail"]
