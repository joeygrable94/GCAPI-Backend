from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


async def test_public_status(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    response: Response = await client.get("/status", headers=admin_token_headers)
    status: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert status == {"status": "ok"}
