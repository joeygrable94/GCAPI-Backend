import pytest
from pydantic import UUID4
from usp.objects.page import SitemapPage  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import create_or_update_website_page, save_sitemap_pages
from app.core.utilities.uuids import get_uuid
from app.crud.website_map import WebsiteMapRepository
from app.models.website_map import WebsiteMap
from app.schemas import WebsiteMapPage

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
    page_b = SitemapPage(url=page_url, priority=0.25)
    page_c = SitemapPage(url=page_url, priority=0.4)
    output_a = await create_or_update_website_page(website_id, sitemap_id, page)  # type: ignore  # noqa: E501
    output_b = await create_or_update_website_page(website_id, sitemap_id, page)  # type: ignore  # noqa: E501
    output_c = await create_or_update_website_page(website_id, sitemap_id, page_b)  # type: ignore  # noqa: E501
    output_d = await create_or_update_website_page(website_id, sitemap_id, page_c)  # type: ignore  # noqa: E501
    assert output_a is None
    assert output_b is None
    assert output_c is None
    assert output_d is None


'''
async def test_save_sitemap_pages(db_session: AsyncSession) -> None:
    website_id = get_uuid()
    sitemap_url = "https://getcommunity.com/"
    sitemap_pages = [
        WebsiteMapPage(url="https://getcommunity.com/products/", priority=0.8, last_modified="2022-10-24 15:00:00+00:00"),
        WebsiteMapPage(url="https://getcommunity.com/products/gc-video/", priority=0.8, last_modified="2022-10-24 15:00:00+00:00"),
        WebsiteMapPage(url="https://getcommunity.com/products/media/", priority=0.8, last_modified="2022-10-24 15:00:00+00:00"),
        WebsiteMapPage(url="https://getcommunity.com/products/gc-text/", priority=0.8, last_modified="2022-10-24 15:00:00+00:00"),
    ]
    sitemap_id = await save_sitemap_pages(website_id, sitemap_url, sitemap_pages)
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(db_session)
    sitemap: WebsiteMap | None = await sitemap_repo.read(sitemap_id)
    assert sitemap
    assert sitemap.id == sitemap_id
'''
