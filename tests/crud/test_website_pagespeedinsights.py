import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import WebsitePageSpeedInsightsRepository
from app.models import WebsitePageSpeedInsights

pytestmark = pytest.mark.asyncio


async def test_website_pagespeedinsights_repo_table(db_session: AsyncSession) -> None:
    repo: WebsitePageSpeedInsightsRepository = WebsitePageSpeedInsightsRepository(
        session=db_session
    )
    assert repo._table is WebsitePageSpeedInsights
