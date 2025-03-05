import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.website_go_ga4.crud import WebsiteGoAnalytics4PropertyRepository
from app.entities.website_go_ga4.model import WebsiteGoAnalytics4Property

pytestmark = pytest.mark.anyio


async def test_organization_websites_repo_table(db_session: AsyncSession) -> None:
    repo: WebsiteGoAnalytics4PropertyRepository = WebsiteGoAnalytics4PropertyRepository(
        session=db_session
    )
    assert repo._table is WebsiteGoAnalytics4Property
