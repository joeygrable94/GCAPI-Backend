from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import WebsitePageRepository
from app.models import Website, WebsitePage
from app.schemas import WebsiteMapRead, WebsitePageCreate, WebsitePageRead, WebsiteRead
from tests.utils.utils import random_lower_string
from tests.utils.website_maps import create_random_website_map
from tests.utils.websites import create_random_website


async def create_random_website_page(
    db_session: AsyncSession,
    website_id: UUID4 | None = None,
    sitemap_id: UUID4 | None = None,
    path: str | None = None,
) -> WebsitePageRead:
    repo: WebsitePageRepository = WebsitePageRepository(session=db_session)
    page_path = "/%s/" % random_lower_string() if path is None else path
    if website_id is None:
        website: Website | WebsiteRead = await create_random_website(db_session)
        website_id = website.id
    if sitemap_id is None:
        website_map: WebsiteMapRead = await create_random_website_map(
            db_session, website_id=website_id
        )
        sitemap_id = website_map.id
    website_page: WebsitePage = await repo.create(
        schema=WebsitePageCreate(
            url=page_path,
            status=200,
            priority=0.5,
            last_modified=None,
            change_frequency=None,
            website_id=website_id,
            sitemap_id=sitemap_id,
        )
    )
    return WebsitePageRead.model_validate(website_page)
