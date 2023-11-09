import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_pagespeedinsights import (
    create_random_website_page_speed_insights,
)

from app.api.deps import get_website_page_psi_or_404
from app.api.exceptions.exceptions import InvalidID
from app.api.exceptions.exceptions import WebsitePageSpeedInsightsNotExists
from app.models.website_pagespeedinsights import WebsitePageSpeedInsights
from app.schemas import WebsitePageSpeedInsightsRead


async def test_get_website_page_psi_or_404(db_session: AsyncSession) -> None:
    # Test with valid website_page_id
    test_website_page_speed_insight: WebsitePageSpeedInsightsRead
    test_website_page_speed_insight = await create_random_website_page_speed_insights(
        db_session
    )
    result: WebsitePageSpeedInsights | None = await get_website_page_psi_or_404(
        db_session, test_website_page_speed_insight.id
    )
    assert isinstance(result, WebsitePageSpeedInsights)
    assert result.id == test_website_page_speed_insight.id

    # Test with invalid website_page_id
    fake_clid: str = "1"
    with pytest.raises(InvalidID):
        await get_website_page_psi_or_404(db_session, fake_clid)

    # Test with invalid website_page_id that looks like a valid uuid
    fake_clid_uuid: str = "00000000-0000-0000-0000-000000000000"
    with pytest.raises(WebsitePageSpeedInsightsNotExists):
        await get_website_page_psi_or_404(db_session, fake_clid_uuid)
