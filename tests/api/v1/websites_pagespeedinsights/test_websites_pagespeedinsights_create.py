"""
from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
# from app.models.website_pagespeedinsights import WebsitePageSpeedInsights
# from tests.utils.website_pagespeedinsights import create_random_website_page_speed_insights

# from app.api.errors import ErrorCode
# from app.core.utilities.uuids import get_uuid_str
# from app.crud import WebsitePageSpeedInsightsRepository
from app.schemas import (
    WebsitePageSpeedInsightsBase,
    WebsiteRead,
    WebsitePageRead,
    WebsiteMapRead,
)
from tests.utils.website_maps import create_random_website_map

from tests.utils.websites import create_random_website
from tests.utils.website_pages import create_random_website_page
from tests.utils.website_pagespeedinsights import generate_psi_base

pytestmark = pytest.mark.asyncio


async def test_create_website_pagespeedinsights_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_website: WebsiteRead = await create_random_website(db_session)
    a_sitemap: WebsiteMapRead = await create_random_website_map(db_session, website_id=a_website.id)
    a_webpage: WebsitePageRead = await create_random_website_page(
        db_session, website_id=a_website.id, sitemap_id=a_sitemap.id
    )
    d_strategy: str = "mobile"
    psi_base: WebsitePageSpeedInsightsBase = generate_psi_base(device_strategy=d_strategy)
    response: Response = await client.post(
        f"psi/?website_id={a_webpage.id}&page_id={a_webpage.id}",
        headers=superuser_token_headers,
        json=psi_base.dict(),
    )
    data: Dict[str, Any] = response.json()
    print(data)
    assert 200 <= response.status_code < 300
    assert data["id"] is not None
    assert data["strategy"] == d_strategy
    assert data["website_id"] == str(a_website.id)
    assert data["page_id"] == str(a_webpage.id)
    # repo: WebsitePageSpeedInsightsRepository = WebsitePageSpeedInsightsRepository(db_session)
    # existing_data: WebsitePageSpeedInsights | None = await repo.read(entry_id=data["id"])
    # assert existing_data
    # assert data["strategy"] == existing_data.strategy
    # assert data["website_id"] == str(existing_data.website_id)
    # assert data["page_id"] == str(existing_data.page_id)


async def test_read_website_pagespeedinsights_by_id_as_superuser_page_not_found(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"psi/{entry_id}",
        headers=superuser_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.WEBSITE_PAGE_SPEED_INSIGHTS_NOT_FOUND
"""
