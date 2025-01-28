from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import WebsiteGoAnalytics4PropertyRepository, WebsiteRepository
from app.models import GoAnalytics4Property, Website, WebsiteGoAnalytics4Property
from app.schemas import (
    GoAnalytics4PropertyRead,
    SitemapPageChangeFrequency,
    WebsiteCreate,
    WebsiteGoAnalytics4PropertyCreate,
    WebsiteMapPage,
    WebsiteRead,
)
from tests.utils.utils import random_boolean, random_domain


async def create_random_website(
    db_session: AsyncSession,
    domain: str | None = None,
    is_secure: bool = random_boolean(),
    return_db_obj: bool = False,
) -> WebsiteRead | Website:
    repo: WebsiteRepository = WebsiteRepository(session=db_session)
    if domain is None:
        domain = random_domain()
    website: Website = await repo.create(
        schema=WebsiteCreate(domain=domain, is_secure=is_secure)
    )
    return WebsiteRead.model_validate(website) if not return_db_obj else website


def build_sitemap_page_meta(
    mock_fetch_sitemap_page_urlset: list[dict[str, Any]],
) -> list[WebsiteMapPage]:
    sitemap_pages = []
    for page in mock_fetch_sitemap_page_urlset:
        page_meta = WebsiteMapPage(
            url=page["url"],
            last_modified=page["lastmod"],
            change_frequency=SitemapPageChangeFrequency(page["changefreq"]),
            priority=page["priority"],
        )
        sitemap_pages.append(page_meta)
    return sitemap_pages


async def assign_ga4_to_website(
    db_session: AsyncSession,
    go_a4: GoAnalytics4Property | GoAnalytics4PropertyRead,
    website: Website | WebsiteRead,
) -> WebsiteGoAnalytics4Property:
    repo = WebsiteGoAnalytics4PropertyRepository(session=db_session)
    website_go_a4: WebsiteGoAnalytics4Property = await repo.create(
        schema=WebsiteGoAnalytics4PropertyCreate(
            website_id=website.id, go_a4_id=go_a4.id
        )
    )
    return website_go_a4
