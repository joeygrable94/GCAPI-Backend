import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.tracking_link.crud import TrackingLinkRepository
from app.entities.tracking_link.model import TrackingLink

pytestmark = pytest.mark.asyncio


async def test_organization_platform_repo_table(db_session: AsyncSession) -> None:
    repo: TrackingLinkRepository = TrackingLinkRepository(session=db_session)
    assert repo._table is TrackingLink
