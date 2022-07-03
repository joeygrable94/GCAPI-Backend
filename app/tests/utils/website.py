from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.website import WebsitesRepository
from app.db.schemas import WebsiteCreate, WebsiteRead
from app.tests.utils.utils import random_lower_string


async def create_random_website(db_session: AsyncSession) -> WebsiteRead:
    domain: str = random_lower_string()
    is_secure: bool = False
    websites_repo: WebsitesRepository = WebsitesRepository(session=db_session)
    website: WebsiteRead = await websites_repo.create(
        WebsiteCreate(domain=domain, is_secure=is_secure)
    )
    return website
