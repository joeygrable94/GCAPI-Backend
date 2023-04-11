import json
from typing import Iterator
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from usp.objects.page import SitemapPage  # type: ignore

from tests.utils.websites import create_random_website
from tests.utils.utils import random_domain

from app.crud import WebsiteMapRepository
from app.models import WebsiteMap
from app.schemas import WebsiteMapCreate, WebsiteMapRead, WebsiteRead


class MockSitemap:
    def __init__(self, url, pages) -> None:
        self.url = url
        self.pages = pages

    def all_pages(self) -> Iterator[SitemapPage]:
        for pg in self.pages:
            yield SitemapPage(pg)


def generate_mock_sitemap(sitemap_url: str, mock_sitemap_str: str):
    pages = json.dumps(mock_sitemap_str, indent=4)
    return MockSitemap(sitemap_url, pages)


async def create_random_website_map(
    db_session: AsyncSession,
    website_id: UUID4 | None = None,
) -> WebsiteMapRead:
    repo: WebsiteMapRepository = WebsiteMapRepository(session=db_session)
    domain: str
    if website_id is None:
        website: WebsiteRead = await create_random_website(db_session)
        website_id=website.id
        domain = website.domain
    else:
        domain = random_domain()
    website_map: WebsiteMap = await repo.create(
        schema=WebsiteMapCreate(url=domain, website_id=website_id)
    )
    return WebsiteMapRead.from_orm(website_map)
