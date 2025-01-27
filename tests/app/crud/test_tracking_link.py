import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import TrackingLinkRepository
from app.models import TrackingLink

pytestmark = pytest.mark.asyncio


async def test_client_platform_repo_table(db_session: AsyncSession) -> None:
    repo: TrackingLinkRepository = TrackingLinkRepository(session=db_session)
    assert repo._table is TrackingLink
