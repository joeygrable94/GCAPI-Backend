import unittest.mock

import pytest
from lxml import etree
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.website_sitemap.crud import WebsiteMapRepository
from app.entities.website_sitemap.model import WebsiteMap

pytestmark = pytest.mark.asyncio


async def test_website_map_repo_is_sitemap_url_xml_invalid_content(
    db_session: AsyncSession,
) -> None:
    repo: WebsiteMapRepository = WebsiteMapRepository(session=db_session)
    with unittest.mock.patch(
        "app.entities.website_sitemap.utilities.fetch_url_status_code"
    ) as mock_fetch_url_status_code:
        mock_fetch_url_status_code.return_value = 200
        with unittest.mock.patch(
            "app.entities.website_sitemap.utilities.check_is_xml_valid_sitemap"
        ) as mock_check_is_xml_valid_sitemap:
            mock_check_is_xml_valid_sitemap.return_value = False
            is_valid = repo.is_sitemap_url_xml_valid(
                url="https://getcommunity.com/sitemap-invalid.xml"
            )
            assert is_valid is False


async def test_website_map_repo_table(db_session: AsyncSession) -> None:
    repo: WebsiteMapRepository = WebsiteMapRepository(session=db_session)
    assert repo._table is WebsiteMap


async def test_website_map_repo_is_sitemap_url_xml_valid(
    db_session: AsyncSession,
) -> None:
    repo: WebsiteMapRepository = WebsiteMapRepository(session=db_session)
    is_valid: bool = repo.is_sitemap_url_xml_valid(
        url="https://getcommunity.com/sitemap.xml"
    )
    assert is_valid is True


async def test_website_map_repo_is_sitemap_url_xml_not_valid(
    db_session: AsyncSession,
) -> None:
    repo: WebsiteMapRepository = WebsiteMapRepository(session=db_session)
    is_valid: bool = repo.is_sitemap_url_xml_valid(
        url="https://getcommunity.com/sitemap-invalid.xml"
    )
    assert is_valid is False


async def test_website_map_repo_is_sitemap_url_xml_invalid_xml_parse(
    db_session: AsyncSession, mock_invalid_sitemap_xml: etree._Element
) -> None:
    repo: WebsiteMapRepository = WebsiteMapRepository(session=db_session)
    with unittest.mock.patch(
        "app.entities.website_page.utilities.fetch_url_status_code"
    ) as mock_fetch_url_status_code:
        mock_fetch_url_status_code.return_value = 200
        with unittest.mock.patch(
            "app.entities.website_sitemap.utilities.fetch_url_page_text"
        ) as mock_fetch_url_page_text:
            mock_fetch_url_page_text.return_value = ""
        with unittest.mock.patch(
            "app.entities.website_sitemap.utilities.parse_sitemap_xml"
        ) as mock_parse_sitemap_xml:
            mock_parse_sitemap_xml.return_value = mock_invalid_sitemap_xml
            is_valid = repo.is_sitemap_url_xml_valid(
                url="https://example.com/sitemap.xml"
            )
            assert is_valid is False


async def test_website_map_repo_is_sitemap_url_xml_invalid_xml_exception_raised(
    db_session: AsyncSession, mock_invalid_sitemap_xml: etree._Element
) -> None:
    repo: WebsiteMapRepository = WebsiteMapRepository(session=db_session)
    with unittest.mock.patch(
        "app.entities.website_page.utilities.fetch_url_status_code"
    ) as mock_fetch_url_status_code:
        mock_fetch_url_status_code.return_value = 200
        with unittest.mock.patch(
            "app.entities.website_sitemap.utilities.fetch_url_page_text"
        ) as mock_fetch_url_page_text:
            mock_fetch_url_page_text.return_value = ""
        with unittest.mock.patch(
            "app.entities.website_sitemap.utilities.parse_sitemap_xml"
        ) as mock_parse_sitemap_xml:
            mock_parse_sitemap_xml.return_value = mock_invalid_sitemap_xml
            with unittest.mock.patch(
                "app.entities.website_sitemap.utilities.check_is_xml_valid_sitemap"
            ) as mock_check_is_xml_valid_sitemap:
                mock_check_is_xml_valid_sitemap.return_value = False
                is_valid = repo.is_sitemap_url_xml_valid(
                    url="https://example.com/sitemap.xml"
                )
                assert is_valid is False
