from time import sleep
from typing import Any, Dict
from unittest.mock import patch

import pytest
from httpx import AsyncClient
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
    celery_worker: Any,
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
) -> None:
    speak_word: str = random_lower_string()
    sleep(5)
    request = await client.get(
        f"/status?message={speak_word}", headers=admin_token_headers
    )
    req_data = request.json()
    assert req_data["status"] == "ok"
    task_id = req_data["speak_task_id"]
    assert task_id
    sleep(5)
    response = await client.get(f"tasks/{task_id}", headers=admin_token_headers)
    response_json: Dict[str, Any] = response.json()
    assert response_json == {
        "task_id": task_id,
        "task_status": "PENDING",
        "task_result": None,
    }
    assert response.status_code == 200
    with patch(
        "app.api.v1.endpoints.tasks.AsyncResult",
        return_value=MockAsyncResult(id=task_id),
    ) as mock_async_result:
        response = await client.get(f"tasks/{task_id}", headers=admin_token_headers)
        assert response.status_code == 200
        data: Dict[str, Any] = response.json()
        assert data == {
            "task_id": str(task_id),
            "task_status": "SUCCESS",
            "task_result": "hello world",
        }
        mock_async_result.assert_called_with(task_id)
