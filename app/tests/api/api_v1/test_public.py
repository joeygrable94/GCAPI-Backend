import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_status(client: AsyncClient) -> None:
    response = await client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
