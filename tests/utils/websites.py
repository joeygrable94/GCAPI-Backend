from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_boolean, random_domain

from app.crud import WebsiteRepository
from app.models import Website
from app.schemas import (
    SitemapPageChangeFrequency,
    WebsiteCreate,
    WebsiteMapPage,
    WebsiteRead,
)


async def create_random_website(
    db_session: AsyncSession, return_db_obj: bool = False
) -> WebsiteRead | Website:
    repo: WebsiteRepository = WebsiteRepository(session=db_session)
    website: Website = await repo.create(
        schema=WebsiteCreate(domain=random_domain(), is_secure=random_boolean())
    )
    return WebsiteRead.model_validate(website) if not return_db_obj else website


def build_sitemap_page_meta(
    mock_fetch_sitemap_page_urlset: list[Dict[str, Any]]
) -> list[WebsiteMapPage]:
    sitemap_pages = []
    for page in mock_fetch_sitemap_page_urlset:
        page_meta = WebsiteMapPage(
            url=page["url"],
            lastmod=page["last_modified"],
            changefreq=SitemapPageChangeFrequency(page["change_frequency"]),
            priority=page["priority"],
        )
        sitemap_pages.append(page_meta)
    return sitemap_pages
