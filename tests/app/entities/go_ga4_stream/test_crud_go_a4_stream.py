import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.go_ga4_stream.crud import GoAnalytics4StreamRepository
from app.entities.go_ga4_stream.model import GoAnalytics4Stream

pytestmark = pytest.mark.anyio


async def test_go_a4_stream_repo_table(db_session: AsyncSession) -> None:
    repo: GoAnalytics4StreamRepository = GoAnalytics4StreamRepository(
        session=db_session
    )
    assert repo._table is GoAnalytics4Stream
