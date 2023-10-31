import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoAnalytics4PropertyRepository
from app.models import GoAnalytics4Property

pytestmark = pytest.mark.asyncio


async def test_go_a4_property_repo_table(db_session: AsyncSession) -> None:
    repo: GoAnalytics4PropertyRepository = GoAnalytics4PropertyRepository(
        session=db_session
    )
    assert repo._table is GoAnalytics4Property
