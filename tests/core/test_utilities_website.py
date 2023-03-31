import pytest
from pydantic import UUID4
from usp.objects.page import SitemapPage  # type: ignore

from app.api.utils import create_or_update_website_page
from app.core.utilities.uuids import get_uuid

pytestmark = pytest.mark.asyncio


async def test_create_or_update_website_page_create() -> None:
    page_url = "https://getcommunity.com/"
    website_id: UUID4 = get_uuid()
    sitemap_id: UUID4 = get_uuid()
    page = SitemapPage(url=page_url, priority=0.5)
    output = await create_or_update_website_page(website_id, sitemap_id, page)  # type: ignore  # noqa: E501
    assert output is None


async def test_create_or_update_website_page_create_then_update() -> None:
    page_url = "https://getcommunity.com/"
    website_id: UUID4 = get_uuid()
    sitemap_id: UUID4 = get_uuid()
    page = SitemapPage(url=page_url, priority=0.5)
    output_a = await create_or_update_website_page(website_id, sitemap_id, page)  # type: ignore  # noqa: E501
    output_b = await create_or_update_website_page(website_id, sitemap_id, page)  # type: ignore  # noqa: E501
    assert output_a is None
    assert output_b is None
