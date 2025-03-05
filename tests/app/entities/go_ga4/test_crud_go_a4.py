import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.go_ga4.crud import GoAnalytics4PropertyRepository
from app.entities.go_ga4.model import GoAnalytics4Property

pytestmark = pytest.mark.anyio


async def test_go_a4_property_repo_table(db_session: AsyncSession) -> None:
    repo: GoAnalytics4PropertyRepository = GoAnalytics4PropertyRepository(
        session=db_session
    )
    assert repo._table is GoAnalytics4Property
