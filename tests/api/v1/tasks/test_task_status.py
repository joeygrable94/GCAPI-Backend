"""
from typing import Any, Dict
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from app.core.utilities import get_uuid
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


async def test_get_status_task_speak(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    speak_word: str = random_lower_string()
    request = await client.get(f"/status?speak={speak_word}", headers=superuser_token_headers)
    req_data = request.json()
    assert req_data["status"] == "ok"
    task_id = req_data["speak_task_id"]
    assert task_id
    response = await client.get(f"tasks/{task_id}", headers=superuser_token_headers)
    content: Dict[str, Any] = response.json()
    assert content == {
        "task_id": task_id,
        "task_status": "PENDING",
        "task_result": None,
    }
    assert response.status_code == 200
    while content["task_status"] == "PENDING":
        response = await client.get(f"tasks/{task_id}", headers=superuser_token_headers)
        content = response.json()
    assert content == {
        "task_id": task_id,
        "task_status": "SUCCESS",
        "task_result": f"I say, {speak_word}!"
    }
    assert response.status_code == 200
"""