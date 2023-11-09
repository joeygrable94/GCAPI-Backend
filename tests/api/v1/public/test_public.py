from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response

pytestmark = pytest.mark.asyncio


async def test_status(client: AsyncClient) -> None:
    response: Response = await client.get("status")
    status: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert status == {"status": "ok"}
