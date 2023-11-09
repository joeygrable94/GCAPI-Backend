from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_boolean
from tests.utils.utils import random_domain

from app.crud import WebsiteRepository
from app.models import Website
from app.schemas import WebsiteCreate
from app.schemas import WebsiteRead


async def create_random_website(db_session: AsyncSession) -> WebsiteRead:
    repo: WebsiteRepository = WebsiteRepository(session=db_session)
    website: Website = await repo.create(
        schema=WebsiteCreate(domain=random_domain(), is_secure=random_boolean())
    )
    return WebsiteRead.model_validate(website)
