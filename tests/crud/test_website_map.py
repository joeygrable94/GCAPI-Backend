import unittest.mock

import pytest
from lxml import etree
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import WebsiteMapRepository
from app.models import WebsiteMap

pytestmark = pytest.mark.asyncio


async def test_website_map_repo_table(db_session: AsyncSession) -> None:
    repo: WebsiteMapRepository = WebsiteMapRepository(session=db_session)
    assert repo._table is WebsiteMap


async def test_website_map_repo_is_sitemap_url_xml_invalid(
    db_session: AsyncSession,
) -> None:
    repo: WebsiteMapRepository = WebsiteMapRepository(session=db_session)
    is_valid: bool = repo.is_sitemap_url_xml_valid(
        url="https://example.com/sitemap.xml"
    )
    assert is_valid is False


async def test_website_map_repo_is_sitemap_url_xml_invalid_xml_parse(
    db_session: AsyncSession, mock_invalid_sitemap_xml: etree._Element
) -> None:
    repo: WebsiteMapRepository = WebsiteMapRepository(session=db_session)
    with unittest.mock.patch(
        "app.core.utilities.websites.fetch_url_status_code"
    ) as mock_fetch_url_status_code:
        mock_fetch_url_status_code.return_value = 200
        with unittest.mock.patch(
            "app.core.utilities.websites.fetch_url_page_text"
        ) as mock_fetch_url_page_text:
            mock_fetch_url_page_text.return_value = ""
        with unittest.mock.patch(
            "app.core.utilities.websites.parse_sitemap_xml"
        ) as mock_parse_sitemap_xml:
            mock_parse_sitemap_xml.return_value = mock_invalid_sitemap_xml
            is_valid: bool = repo.is_sitemap_url_xml_valid(
                url="https://example.com/sitemap.xml"
            )
            assert is_valid is False


async def test_website_map_repo_is_sitemap_url_xml_invalid_xml_exception_raised(
    db_session: AsyncSession, mock_invalid_sitemap_xml: etree._Element
) -> None:
    repo: WebsiteMapRepository = WebsiteMapRepository(session=db_session)
    with unittest.mock.patch(
        "app.core.utilities.websites.fetch_url_status_code"
    ) as mock_fetch_url_status_code:
        mock_fetch_url_status_code.return_value = 200
        with unittest.mock.patch(
            "app.core.utilities.websites.fetch_url_page_text"
        ) as mock_fetch_url_page_text:
            mock_fetch_url_page_text.return_value = ""
        with unittest.mock.patch(
            "app.core.utilities.websites.parse_sitemap_xml"
        ) as mock_parse_sitemap_xml:
            mock_parse_sitemap_xml.return_value = mock_invalid_sitemap_xml
            with unittest.mock.patch(
                "app.core.utilities.websites.check_is_xml_valid_sitemap"
            ) as mock_check_is_xml_valid_sitemap:
                mock_check_is_xml_valid_sitemap.return_value = False
                with pytest.raises(Exception) as exc_info:
                    is_valid: bool = repo.is_sitemap_url_xml_valid(
                        url="https://example.com/sitemap.xml"
                    )
                    assert is_valid is False
                    # check that the function is_sitemap_url_xml_valid was called
                    assert mock_check_is_xml_valid_sitemap.called is True
                    assert exc_info.value.args[0] == "Invalid Sitemap XML"
