from lxml import etree

from app.entities.website_sitemap.utilities import (
    check_is_sitemap_page,
    check_is_sitemap_urlset,
    check_is_xml_valid_sitemap,
    fetch_url_page_text,
)


def test_fetch_url_page_text() -> None:
    html = fetch_url_page_text("https://getcommunity.com/sitemap.xml")
    assert html is not None


def test_check_is_xml_valid_sitemap_true(
    mock_valid_sitemap_urlset_xml: etree._Element,
) -> None:
    result = check_is_xml_valid_sitemap(mock_valid_sitemap_urlset_xml)
    assert result is True


def test_check_is_xml_valid_sitemap_false(
    mock_invalid_sitemap_xml: etree._Element,
) -> None:
    result = check_is_xml_valid_sitemap(mock_invalid_sitemap_xml)
    assert result is False


def test_check_is_sitemap_page_false(
    mock_invalid_sitemap_xml: etree._Element,
) -> None:
    result = check_is_sitemap_page(mock_invalid_sitemap_xml)
    assert result is False


def test_check_is_sitemap_urlset_false(
    mock_invalid_sitemap_xml: etree._Element,
) -> None:
    result = check_is_sitemap_urlset(mock_invalid_sitemap_xml)
    assert result is False


async def test_check_is_sitemap_urlset_true(
    mock_valid_sitemap_urlset_xml: etree._Element,
) -> None:
    result = check_is_sitemap_urlset(mock_valid_sitemap_urlset_xml)
    assert result is True
