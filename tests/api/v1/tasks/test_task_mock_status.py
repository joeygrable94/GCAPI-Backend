from typing import Any, Dict
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from app.core.utilities import get_uuid_str

pytestmark = pytest.mark.asyncio


class MockAsyncResult:
    def __init__(self, id: Any) -> None:
        self.id: str = id
        self.status: str = "SUCCESS"
        self.result: Any = "hello world"

    async def __call__(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        return self


async def test_get_status(
    celery_worker: Any,
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
) -> None:
    task_id = get_uuid_str()
    task_state = MockAsyncResult(id=task_id)

    with patch(
        "app.api.v1.endpoints.tasks.AsyncResult", return_value=task_state
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
