from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


class MockAsyncResult:
    def __init__(self, id: Any) -> None:
        self.id: str = id
        self.status: str = "SUCCESS"
        self.result: Any = "hello world"

    async def __call__(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        return self


async def test_get_status_task_speak(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    speak_word: str = random_lower_string()
    request = await client.get(
        f"/status?message={speak_word}", headers=admin_token_headers
    )
    req_data = request.json()
    assert req_data["status"] == "ok"
    task_id = req_data["speak_task_id"]
    assert task_id
    response = await client.get(f"tasks/{task_id}", headers=admin_token_headers)
    response_json: Dict[str, Any] = response.json()
    assert response_json["task_id"] == task_id
    assert response_json["task_status"] == "PENDING"
    assert response_json["task_time"] == 0.0
    assert response_json["task_result"] is None
    assert response.status_code == 200
