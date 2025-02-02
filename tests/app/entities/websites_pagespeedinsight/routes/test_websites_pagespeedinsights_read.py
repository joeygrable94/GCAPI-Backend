from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import ERROR_MESSAGE_ENTITY_NOT_FOUND
from app.entities.website_pagespeedinsight.crud import (
    WebsitePageSpeedInsightsRepository,
)
from app.utilities import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.website_pagespeedinsights import (
    create_random_website_page_speed_insights,
)

pytestmark = pytest.mark.asyncio


async def test_read_website_pagespeedinsights_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    entry = await create_random_website_page_speed_insights(db_session)
    response: Response = await client.get(
        f"psi/{entry.id}", headers=admin_user.token_headers
    )
    data: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    assert data["strategy"] == entry.strategy
    assert data["website_id"] == str(entry.website_id)
    assert data["page_id"] == str(entry.page_id)
    repo = WebsitePageSpeedInsightsRepository(db_session)
    existing_data = await repo.read(entry.id)
    assert existing_data
    assert data["strategy"] == existing_data.strategy
    assert data["website_id"] == str(existing_data.website_id)
    assert data["page_id"] == str(existing_data.page_id)


async def test_read_website_pagespeedinsights_by_id_as_superuser_page_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"psi/{entry_id}", headers=admin_user.token_headers
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]
