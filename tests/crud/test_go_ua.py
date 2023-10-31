import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoUniversalAnalyticsPropertyRepository
from app.models import GoUniversalAnalyticsProperty

pytestmark = pytest.mark.asyncio


async def test_go_ua_property_repo_table(db_session: AsyncSession) -> None:
    repo: GoUniversalAnalyticsPropertyRepository = (
        GoUniversalAnalyticsPropertyRepository(session=db_session)
    )
    assert repo._table is GoUniversalAnalyticsProperty
