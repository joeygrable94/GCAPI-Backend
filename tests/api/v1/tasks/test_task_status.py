from typing import Any, Dict

import pytest
from httpx import AsyncClient
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


async def test_get_status_task_speak(
    celery_worker: Any,
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    speak_word: str = random_lower_string()
    request = await client.get(
        f"/status?speak={speak_word}", headers=superuser_token_headers
    )
    req_data = request.json()
    assert req_data["status"] == "ok"
    task_id = req_data["speak_task_id"]
    assert task_id
    response = await client.get(f"tasks/{task_id}", headers=superuser_token_headers)
    response_json: Dict[str, Any] = response.json()
    assert response_json == {
        "task_id": task_id,
        "task_status": "PENDING",
        "task_result": None,
    }
    assert response.status_code == 200

    """
    while response_json["task_status"] == "PENDING":
        response = await client.get(
            f"tasks/{task_id}",
            headers=superuser_token_headers
        )
        response_json = response.json()
    assert response_json == {
        "task_id": task_id,
        "task_status": "SUCCESS",
        "task_result": f"I say, {speak_word}!"
    }
    assert response.status_code == 200
    """
