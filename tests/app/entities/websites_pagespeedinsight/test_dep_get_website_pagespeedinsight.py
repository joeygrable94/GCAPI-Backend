import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.errors import EntityNotFound, InvalidID
from app.entities.website_pagespeedinsight.dependencies import (
    get_website_page_psi_or_404,
)
from app.entities.website_pagespeedinsight.model import WebsitePageSpeedInsights
from app.entities.website_pagespeedinsight.schemas import WebsitePageSpeedInsightsRead
from tests.utils.website_pagespeedinsights import (
    create_random_website_page_speed_insights,
)


async def test_get_website_page_psi_or_404(db_session: AsyncSession) -> None:
    # Test with valid website_page_id
    test_website_page_speed_insight: WebsitePageSpeedInsightsRead
    test_website_page_speed_insight = await create_random_website_page_speed_insights(
        db_session
    )
    result = await get_website_page_psi_or_404(
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
    with pytest.raises(EntityNotFound):
        await get_website_page_psi_or_404(db_session, fake_clid_uuid)
