from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import ERROR_MESSAGE_ENTITY_NOT_FOUND
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.website_pagespeedinsights import (
    create_random_website_page_speed_insights,
)

pytestmark = pytest.mark.asyncio


async def test_delete_website_pagespeedinsights_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    entry = await create_random_website_page_speed_insights(db_session)
    response: Response = await client.delete(
        f"psi/{entry.id}", headers=admin_user.token_headers
    )
    assert 200 <= response.status_code < 300
    response: Response = await client.get(
        f"psi/{entry.id}", headers=admin_user.token_headers
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]
