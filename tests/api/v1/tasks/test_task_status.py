from typing import Any, Dict
from unittest.mock import patch

from httpx import AsyncClient
import pytest

from tests.utils.utils import random_lower_string
from app.core.utilities import get_uuid_str
from app.worker import task_speak

pytestmark = pytest.mark.asyncio


class MockAsyncResult:
    def __init__(self, id: Any) -> None:
        self.id: Any = id
        self.status: Any = "SUCCESS"
        self.result: Any = "hello world"

    async def __call__(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        return self


async def test_get_status(client: AsyncClient, superuser_token_headers: Dict[str, str]) -> None:
    task_id = get_uuid_str()
    task_state = MockAsyncResult(id=task_id)

    with patch('app.api.v1.endpoints.tasks.AsyncResult', return_value=task_state) as mock_async_result:
        response = await client.get(f"tasks/{task_id}", headers=superuser_token_headers)
        assert response.status_code == 200
        data: Dict[str, Any] = response.json()
        assert data["task_id"] == task_id
        assert data["task_status"] == "SUCCESS"
        assert data["task_result"] == "hello world"

        mock_async_result.assert_called_once_with(task_id)



@pytest.mark.celery
async def test_get_status_celery_task_speak(
    celery_worker: Any,
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    random_word = random_lower_string()
    result = task_speak.delay(random_word)

    response = await client.get(f"tasks/{result.id}", headers=superuser_token_headers)
    task_data: Dict[str, Any] = response.json()

    assert task_data["task_id"] == result.id
    assert task_data["task_status"] == "PENDING"
    assert task_data["task_result"] == None
