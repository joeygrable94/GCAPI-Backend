import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_maps import create_random_website_map
from tests.utils.websites import create_random_website
from usp.objects.page import SitemapPage  # type: ignore

from app.api.utils import create_or_update_website_page
from app.schemas.website import WebsiteRead
from app.schemas.website_map import WebsiteMapRead

pytestmark = pytest.mark.asyncio


async def test_create_or_update_website_page_create(
    db_session: AsyncSession,
) -> None:
    page_url = "https://getcommunity.com/"
    website: WebsiteRead = await create_random_website(db_session)
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    page = SitemapPage(url=page_url, priority=0.5)
    output = await create_or_update_website_page(website.id, sitemap.id, page)  # type: ignore  # noqa: E501
    assert output is None


async def test_create_or_update_website_page_create_then_update(
    db_session: AsyncSession,
) -> None:
    page_url = "https://getcommunity.com/"
    website: WebsiteRead = await create_random_website(db_session)
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    page = SitemapPage(url=page_url, priority=0.5)
    page_b = SitemapPage(url=page_url, priority=0.25)
    page_c = SitemapPage(url=page_url, priority=0.4)
    output_a = await create_or_update_website_page(website.id, sitemap.id, page)  # type: ignore  # noqa: E501
    output_b = await create_or_update_website_page(website.id, sitemap.id, page)  # type: ignore  # noqa: E501
    output_c = await create_or_update_website_page(website.id, sitemap.id, page_b)  # type: ignore  # noqa: E501
    output_d = await create_or_update_website_page(website.id, sitemap.id, page_c)  # type: ignore  # noqa: E501
    assert output_a is None
    assert output_b is None
    assert output_c is None
    assert output_d is None
