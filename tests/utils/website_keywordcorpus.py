from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.website_keywordcorpus.crud import WebsiteKeywordCorpusRepository
from app.entities.website_keywordcorpus.model import WebsiteKeywordCorpus
from app.entities.website_keywordcorpus.schemas import (
    WebsiteKeywordCorpusCreate,
    WebsiteKeywordCorpusRead,
)
from tests.utils.utils import random_lower_string
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website


async def create_random_website_keywordcorpus(
    db_session: AsyncSession,
    website_id: UUID4 | None,
    page_id: UUID4 | None,
) -> WebsiteKeywordCorpusRead:
    if website_id is None:
        website = await create_random_website(db_session)
        website_id = website.id
    if page_id is None:
        page = await create_random_website_page(db_session, website_id=website_id)
        page_id = page.id
    repo = WebsiteKeywordCorpusRepository(session=db_session)
    website_kwc: WebsiteKeywordCorpus = await repo.create(
        schema=WebsiteKeywordCorpusCreate(
            corpus=random_lower_string(5000),
            rawtext=random_lower_string(10000),
            website_id=website_id,
            page_id=page_id,
        )
    )
    return WebsiteKeywordCorpusRead.model_validate(website_kwc)
