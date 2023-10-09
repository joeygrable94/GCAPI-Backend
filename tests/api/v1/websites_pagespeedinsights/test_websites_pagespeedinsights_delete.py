from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_pagespeedinsights import (
    create_random_website_page_speed_insights,
)

from app.api.exceptions import ErrorCode
from app.schemas import WebsitePageSpeedInsightsRead

pytestmark = pytest.mark.asyncio


async def test_delete_website_pagespeedinsights_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(db_session)
    )
    response: Response = await client.delete(
        f"psi/{entry.id}",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    response: Response = await client.get(
        f"psi/{entry.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.WEBSITE_PAGE_SPEED_INSIGHTS_NOT_FOUND
