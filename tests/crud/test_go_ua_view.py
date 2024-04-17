import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoUniversalAnalyticsViewRepository
from app.models import GoUniversalAnalyticsView

pytestmark = pytest.mark.asyncio


async def test_go_ua_view_repo_table(db_session: AsyncSession) -> None:
    repo: GoUniversalAnalyticsViewRepository = GoUniversalAnalyticsViewRepository(
        session=db_session
    )
    assert repo._table is GoUniversalAnalyticsView
