import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.website_pagespeedinsight.crud import (
    WebsitePageSpeedInsightsRepository,
)
from app.entities.website_pagespeedinsight.model import WebsitePageSpeedInsights

pytestmark = pytest.mark.anyio


async def test_website_pagespeedinsights_repo_table(db_session: AsyncSession) -> None:
    repo: WebsitePageSpeedInsightsRepository = WebsitePageSpeedInsightsRepository(
        session=db_session
    )
    assert repo._table is WebsitePageSpeedInsights
