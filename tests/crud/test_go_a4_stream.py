import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoAnalytics4StreamRepository
from app.models import GoAnalytics4Stream

pytestmark = pytest.mark.asyncio


async def test_go_a4_stream_repo_table(db_session: AsyncSession) -> None:
    repo: GoAnalytics4StreamRepository = GoAnalytics4StreamRepository(
        session=db_session
    )
    assert repo._table is GoAnalytics4Stream
