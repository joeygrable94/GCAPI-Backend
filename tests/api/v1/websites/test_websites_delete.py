from typing import Any, Dict, Optional

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.websites import create_random_website

from app.crud import WebsiteRepository
from app.schemas import WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_delete_website_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry: WebsiteRead = await create_random_website(db_session)
    response: Response = await client.delete(
        f"websites/{entry.id}",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    repo: WebsiteRepository = WebsiteRepository(db_session)
    data_not_found: Optional[Any] = await repo.read_by("domain", entry.domain)
    assert data_not_found is None
