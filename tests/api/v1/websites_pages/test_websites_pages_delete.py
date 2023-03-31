from typing import Any, Dict, Optional

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_pages import create_random_website_page

from app.crud import WebsitePageRepository
from app.schemas import WebsitePageRead

pytestmark = pytest.mark.asyncio


async def test_delete_website_page_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry: WebsitePageRead = await create_random_website_page(db_session)
    response: Response = await client.delete(
        f"webpages/{entry.id}",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    repo: WebsitePageRepository = WebsitePageRepository(db_session)
    data_not_found: Optional[Any] = await repo.read(entry.id)
    assert data_not_found is None
