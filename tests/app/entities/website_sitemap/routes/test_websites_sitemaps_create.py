import unittest.mock
from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_URLPATH_MAXLEN_INPUT
from app.entities.api.constants import (
    ERROR_MESSAGE_ENTITY_EXISTS,
    ERROR_MESSAGE_ENTITY_NOT_FOUND,
)
from app.entities.website_sitemap.constants import ERROR_MESSAGE_XML_INVALID
from app.utilities import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.utils import random_lower_string
from tests.utils.website_maps import create_random_website_map
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


async def test_create_website_sitemap_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session, return_db_obj=True)
    with unittest.mock.patch(
        "app.entities.website_sitemap.crud.WebsiteMapRepository.is_sitemap_url_xml_valid"
    ) as mock_valid_sitemap_xml:
        mock_valid_sitemap_xml.return_value = True
        website_url = a_website.get_link()
        data_2 = {
            "url": f"{website_url}/sitemap.xml",
            "website_id": str(a_website.id),
        }
        response_2: Response = await client.post(
            "sitemaps/",
            headers=admin_user.token_headers,
            json=data_2,
        )
        entry: dict[str, Any] = response_2.json()
        assert 200 <= response_2.status_code < 300
        assert entry["id"] is not None
        assert entry["url"] == data_2["url"]
        assert entry["is_active"] is True
        assert entry["website_id"] == str(a_website.id)


async def test_create_website_sitemap_as_superuser_url_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    sitemap = await create_random_website_map(db_session)
    data = {
        "url": sitemap.url,
        "website_id": str(sitemap.website_id),
    }
    # mock is_sitemap_url_xml_valid
    with unittest.mock.patch(
        "app.entities.website_sitemap.crud.WebsiteMapRepository.is_sitemap_url_xml_valid"
    ) as mock_valid_sitemap_xml:
        mock_valid_sitemap_xml.return_value = True
        response: Response = await client.post(
            "sitemaps/",
            headers=admin_user.token_headers,
            json=data,
        )
        assert response.status_code == 400
        entry: dict[str, Any] = response.json()
        assert ERROR_MESSAGE_ENTITY_EXISTS in entry["detail"]


async def test_create_website_sitemap_as_superuser_unassigned_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    fake_id: str = get_uuid_str()
    sitemap = await create_random_website_map(db_session)
    data = {
        "url": sitemap.url,
        "website_id": fake_id,
    }
    response: Response = await client.post(
        "sitemaps/",
        headers=admin_user.token_headers,
        json=data,
    )
    assert response.status_code == 404
    entry: dict[str, Any] = response.json()
    assert ERROR_MESSAGE_ENTITY_NOT_FOUND in entry["detail"]


async def test_create_website_sitemap_as_superuser_url_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    sitemap = await create_random_website_map(db_session)
    data = {
        "url": "",
        "website_id": str(sitemap.website_id),
    }
    response: Response = await client.post(
        "sitemaps/",
        headers=admin_user.token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "Value error, url is required"


async def test_create_website_sitemap_as_superuser_url_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    long_url: str = random_lower_string(chars=5001)
    sitemap = await create_random_website_map(db_session)
    data = {
        "url": long_url,
        "website_id": str(sitemap.website_id),
    }
    response: Response = await client.post(
        "sitemaps/",
        headers=admin_user.token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, url must be {DB_STR_URLPATH_MAXLEN_INPUT} characters or less"
    )


async def test_create_website_sitemap_as_superuser_url_xml_invalid(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(
        db_session, domain="getcommunity.com", return_db_obj=True
    )
    data = {
        "url": "sitemap-invalid.xml",
        "website_id": str(a_website.id),
    }
    response: Response = await client.post(
        "sitemaps/",
        headers=admin_user.token_headers,
        json=data,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 422
    assert entry["detail"] == ERROR_MESSAGE_XML_INVALID
