from typing import Any, Dict, Optional

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_maps import create_random_website_map

from app.crud import WebsiteMapRepository
from app.schemas import WebsiteMapRead

pytestmark = pytest.mark.asyncio


async def test_delete_website_sitemap_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry: WebsiteMapRead = await create_random_website_map(db_session)
    response: Response = await client.delete(
        f"sitemaps/{entry.id}",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    repo: WebsiteMapRepository = WebsiteMapRepository(db_session)
    data_not_found: Optional[Any] = await repo.read(entry.id)
    assert data_not_found is None
