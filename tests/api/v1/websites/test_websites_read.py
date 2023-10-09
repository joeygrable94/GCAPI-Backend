from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_boolean

from app.api.exceptions import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.schemas import WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_read_website_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = "greatersmc.com"
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data,
    )
    new_website: Dict[str, Any] = response.json()
    entry = WebsiteRead(**new_website["website"])
    response: Response = await client.get(
        f"websites/{entry.id}",
        headers=superuser_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)


async def test_read_website_by_id_as_superuser_website_not_found(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"websites/{entry_id}",
        headers=superuser_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.WEBSITE_NOT_FOUND
