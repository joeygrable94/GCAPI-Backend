import unittest.mock
from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string
from tests.utils.website_maps import create_random_website_map

from app.api.exceptions import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.crud.website import WebsiteRepository
from app.models import Website
from app.schemas import WebsiteMapRead

pytestmark = pytest.mark.asyncio


async def test_create_website_sitemap_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    domain: str = "getcommunity.com"
    is_secure: bool = True
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=admin_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    website_repo: WebsiteRepository = WebsiteRepository(session=db_session)
    website: Website | None = await website_repo.read_by(
        field_name="domain", field_value=domain
    )
    assert website is not None
    # mock is_sitemap_url_xml_valid
    with unittest.mock.patch(
        "app.crud.website_map.WebsiteMapRepository.is_sitemap_url_xml_valid"
    ) as mock_valid_sitemap_xml:
        mock_valid_sitemap_xml.return_value = True
        website_url = website.get_link()
        data_2 = {
            "url": f"{website_url}/sitemap.xml",
            "website_id": str(website.id),
        }
        response_2: Response = await client.post(
            "sitemaps/",
            headers=admin_token_headers,
            json=data_2,
        )
        entry: Dict[str, Any] = response_2.json()
        assert 200 <= response_2.status_code < 300
        assert entry["id"] is not None
        assert entry["url"] == data_2["url"]
        assert entry["is_active"] is True
        assert entry["website_id"] == str(website.id)


async def test_create_website_sitemap_as_superuser_url_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    data = {
        "url": sitemap.url,
        "website_id": str(sitemap.website_id),
    }
    # mock is_sitemap_url_xml_valid
    with unittest.mock.patch(
        "app.crud.website_map.WebsiteMapRepository.is_sitemap_url_xml_valid"
    ) as mock_valid_sitemap_xml:
        mock_valid_sitemap_xml.return_value = True
        response: Response = await client.post(
            "sitemaps/",
            headers=admin_token_headers,
            json=data,
        )
        assert response.status_code == 400
        entry: Dict[str, Any] = response.json()
        assert entry["detail"] == ErrorCode.WEBSITE_MAP_EXISTS


async def test_create_website_sitemap_as_superuser_unassigned_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_id: str = get_uuid_str()
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    data = {
        "url": sitemap.url,
        "website_id": fake_id,
    }
    response: Response = await client.post(
        "sitemaps/",
        headers=admin_token_headers,
        json=data,
    )
    assert response.status_code == 404
    entry: Dict[str, Any] = response.json()
    assert entry["detail"] == ErrorCode.WEBSITE_NOT_FOUND


async def test_create_website_sitemap_as_superuser_url_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    data = {
        "url": "",
        "website_id": str(sitemap.website_id),
    }
    response: Response = await client.post(
        "sitemaps/",
        headers=admin_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "Value error, url is required"


async def test_create_website_sitemap_as_superuser_url_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    long_url: str = random_lower_string(chars=5001)
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    data = {
        "url": long_url,
        "website_id": str(sitemap.website_id),
    }
    response: Response = await client.post(
        "sitemaps/",
        headers=admin_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"] == "Value error, url must be 2048 characters or less"
    )


async def test_create_website_sitemap_as_superuser_xml_url_status_code_error(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    data = {
        "url": sitemap.url,
        "website_id": str(sitemap.website_id),
    }
    # mock fetch_url_status_code
    with unittest.mock.patch(
        "app.core.utilities.websites.fetch_url_status_code"
    ) as mock_fetch_url_status_code:
        mock_fetch_url_status_code.return_value = 404
        response: Response = await client.post(
            "sitemaps/",
            headers=admin_token_headers,
            json=data,
        )
        assert response.status_code == 400
        entry: Dict[str, Any] = response.json()
        assert entry["detail"] == ErrorCode.WEBSITE_MAP_URL_XML_INVALID


async def test_create_website_sitemap_as_superuser_url_xml_invalid(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    data = {
        "url": sitemap.url,
        "website_id": str(sitemap.website_id),
    }
    # mock check_is_xml_valid_sitemap
    with unittest.mock.patch(
        "app.core.utilities.websites.check_is_xml_valid_sitemap"
    ) as mock_check_is_xml_valid_sitemap:
        mock_check_is_xml_valid_sitemap.return_value = False
        response: Response = await client.post(
            "sitemaps/",
            headers=admin_token_headers,
            json=data,
        )
        assert response.status_code == 400
        entry: Dict[str, Any] = response.json()
        assert entry["detail"] == ErrorCode.WEBSITE_MAP_URL_XML_INVALID
