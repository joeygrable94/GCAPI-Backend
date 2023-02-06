from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_boolean, random_domain

from app.db.repositories import WebsiteRepository
from app.db.schemas import WebsiteCreate, WebsiteRead
from app.db.tables import Website


async def create_random_website(db_session: AsyncSession) -> WebsiteRead:
    repo: WebsiteRepository = WebsiteRepository(session=db_session)
    user: Website = await repo.create(
        schema=WebsiteCreate(domain=random_domain(), is_secure=random_boolean())
    )
    return WebsiteRead.from_orm(user)
