from typing import Any
from typing import Dict

import pytest
from httpx import AsyncClient
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_pages import create_random_website_page

from app.api.exceptions import ErrorCode
from app.schemas import WebsitePageRead

pytestmark = pytest.mark.asyncio


async def test_delete_website_page_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry: WebsitePageRead = await create_random_website_page(db_session)
    response: Response = await client.delete(
        f"webpages/{entry.id}",
        headers=admin_token_headers,
    )
    assert 200 <= response.status_code < 300
    response: Response = await client.get(
        f"webpages/{entry.id}",
        headers=admin_token_headers,
    )
    assert response.status_code == 404
    data: Dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.WEBSITE_PAGE_NOT_FOUND
