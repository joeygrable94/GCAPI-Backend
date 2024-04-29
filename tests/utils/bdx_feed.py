from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string

from app.crud import BdxFeedRepository
from app.models import BdxFeed
from app.schemas import BdxFeedCreate, BdxFeedRead


async def create_random_bdx_feed(
    db_session: AsyncSession, client_id: UUID4
) -> BdxFeedRead:
    repo: BdxFeedRepository = BdxFeedRepository(session=db_session)
    bdx_feed: BdxFeed = await repo.create(
        schema=BdxFeedCreate(
            username=random_lower_string(),
            password=random_lower_string(),
            serverhost=random_lower_string(),
            client_id=client_id,
        )
    )
    return BdxFeedRead.model_validate(bdx_feed)
