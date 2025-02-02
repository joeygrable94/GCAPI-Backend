from typing import Any

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.website.crud import WebsiteRepository
from app.entities.website.model import Website
from app.entities.website.schemas import WebsiteCreate, WebsiteRead
from app.entities.website_go_ga4.crud import WebsiteGoAnalytics4PropertyRepository
from app.entities.website_go_ga4.model import WebsiteGoAnalytics4Property
from app.entities.website_go_ga4.schemas import WebsiteGoAnalytics4PropertyCreate
from app.entities.website_go_gads.crud import WebsiteGoAdsPropertyRepository
from app.entities.website_go_gads.model import WebsiteGoAdsProperty
from app.entities.website_go_gads.schemas import WebsiteGoAdsPropertyCreate
from app.entities.website_sitemap.schemas import (
    SitemapPageChangeFrequency,
    WebsiteMapPage,
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
    website = await repo.create(
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
    go_a4_id: UUID4,
    website_id: UUID4,
) -> WebsiteGoAnalytics4Property:
    repo = WebsiteGoAnalytics4PropertyRepository(session=db_session)
    website_go_a4: WebsiteGoAnalytics4Property = await repo.create(
        schema=WebsiteGoAnalytics4PropertyCreate(
            website_id=website_id, go_a4_id=go_a4_id
        )
    )
    return website_go_a4


async def assign_gads_to_website(
    db_session: AsyncSession,
    go_ads_id: UUID4,
    website_id: UUID4,
) -> WebsiteGoAdsProperty:
    repo = WebsiteGoAdsPropertyRepository(session=db_session)
    website_go_a4: WebsiteGoAdsProperty = await repo.create(
        schema=WebsiteGoAdsPropertyCreate(website_id=website_id, go_ads_id=go_ads_id)
    )
    return website_go_a4
