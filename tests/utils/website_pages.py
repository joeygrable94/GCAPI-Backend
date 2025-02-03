from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.website_page.crud import WebsitePageRepository
from app.entities.website_page.model import WebsitePage
from app.entities.website_page.schemas import WebsitePageCreate, WebsitePageRead
from tests.utils.utils import random_lower_string
from tests.utils.websites import create_random_website


async def create_random_website_page(
    db_session: AsyncSession,
    website_id: UUID4 | None = None,
    path: str | None = None,
    is_active: bool = True,
) -> WebsitePageRead:
    repo: WebsitePageRepository = WebsitePageRepository(session=db_session)
    page_path = "/%s/" % random_lower_string() if path is None else path
    if website_id is None:
        website = await create_random_website(db_session)
        website_id = website.id
    website_page: WebsitePage = await repo.create(
        schema=WebsitePageCreate(
            url=page_path,
            status=200,
            priority=0.5,
            last_modified=None,
            change_frequency=None,
            is_active=is_active,
            website_id=website_id,
        )
    )
    return WebsitePageRead.model_validate(website_page)
