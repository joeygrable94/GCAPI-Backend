import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import WebsiteGoAnalytics4PropertyRepository
from app.models import WebsiteGoAnalytics4Property

pytestmark = pytest.mark.asyncio


async def test_clients_websites_repo_table(db_session: AsyncSession) -> None:
    repo: WebsiteGoAnalytics4PropertyRepository = WebsiteGoAnalytics4PropertyRepository(
        session=db_session
    )
    assert repo._table is WebsiteGoAnalytics4Property
