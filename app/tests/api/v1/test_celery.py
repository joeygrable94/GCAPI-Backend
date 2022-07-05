# from typing import Any, Dict

import pytest

# from httpx import AsyncClient, Response

pytestmark = pytest.mark.asyncio


"""
async def test_celery_worker_test(
    client: AsyncClient, superuser_token_headers: Dict[str, str]
) -> None:
    r: Response = await client.post(
        "/utils/test-celery/",
        headers=superuser_token_headers,
        data={"msg": "test"},
    )
    response: Dict[str, Any] = r.json()
    assert response["msg"] == "Word received"
"""
