from typing import Dict

import pytest
from fastapi.testclient import TestClient

from app import config as settings


@pytest.mark.asyncio
async def test_celery_worker_test(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    data = {"msg": "test"}
    r = await client.post(
        f"{settings.API_PREFIX}/utils/test-celery/",
        json=data,
        headers=superuser_token_headers,
    )
    response = r.json()
    assert response["msg"] == "Word received"
