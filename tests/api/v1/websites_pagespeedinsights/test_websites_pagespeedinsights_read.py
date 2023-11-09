from typing import Any
from typing import Dict

import pytest
from httpx import AsyncClient
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_pagespeedinsights import (
    create_random_website_page_speed_insights,
)

from app.api.exceptions import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.crud import WebsitePageSpeedInsightsRepository
from app.models.website_pagespeedinsights import WebsitePageSpeedInsights
from app.schemas import WebsitePageSpeedInsightsRead

pytestmark = pytest.mark.asyncio


async def test_read_website_pagespeedinsights_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry: WebsitePageSpeedInsightsRead = (
        await create_random_website_page_speed_insights(db_session)
    )
    response: Response = await client.get(
        f"psi/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    assert data["strategy"] == entry.strategy
    assert data["website_id"] == str(entry.website_id)
    assert data["page_id"] == str(entry.page_id)
    repo: WebsitePageSpeedInsightsRepository = WebsitePageSpeedInsightsRepository(
        db_session
    )
    existing_data: WebsitePageSpeedInsights | None = await repo.read(entry.id)
    assert existing_data
    assert data["strategy"] == existing_data.strategy
    assert data["website_id"] == str(existing_data.website_id)
    assert data["page_id"] == str(existing_data.page_id)


async def test_read_website_pagespeedinsights_by_id_as_superuser_page_not_found(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"psi/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.WEBSITE_PAGE_SPEED_INSIGHTS_NOT_FOUND
