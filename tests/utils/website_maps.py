from typing import Any, Iterator

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import WebsiteMapRepository
from app.models import Website, WebsiteMap
from app.schemas import WebsiteMapCreate, WebsiteMapPage, WebsiteMapRead, WebsiteRead
from tests.utils.websites import create_random_website


class MockSitemap:
    def __init__(self, url: Any, pages: Any) -> None:
        self.url = url
        self.pages = pages

    def all_pages(self) -> Iterator[WebsiteMapPage]:
        for pg in self.pages:
            yield WebsiteMapPage(
                url=pg.get("url"),
                priority=pg.get("priority"),
                last_modified=pg.get("last_modified"),
            )


def generate_mock_sitemap(sitemap_url: str, mock_sitemap_pages: list) -> MockSitemap:
    return MockSitemap(sitemap_url, mock_sitemap_pages)


async def create_random_website_map(
    db_session: AsyncSession,
    website_id: UUID4 | None = None,
    url_path: str = "sitemap.xml",
) -> WebsiteMapRead:
    repo: WebsiteMapRepository = WebsiteMapRepository(session=db_session)
    if website_id is None:
        website: Website | WebsiteRead = await create_random_website(db_session)
        website_id = website.id
    website_map: WebsiteMap = await repo.create(
        schema=WebsiteMapCreate(url=url_path, website_id=website_id)
    )
    return WebsiteMapRead.model_validate(website_map)
