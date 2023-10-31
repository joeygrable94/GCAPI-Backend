import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BdxFeedRepository
from app.models import BdxFeed

pytestmark = pytest.mark.asyncio


async def test_bdx_feed_repo_table(db_session: AsyncSession) -> None:
    repo: BdxFeedRepository = BdxFeedRepository(session=db_session)
    assert repo._table is BdxFeed
