import pytest
from tests.utils.utils import random_lower_string

from app.tasks import task_speak


@pytest.mark.anyio
async def test_worker_task_speak() -> None:
    random_word = random_lower_string()
    task = await task_speak.kiq(random_word)
    result = await task.wait_result()
    assert result.return_value == f"I say, {random_word}!"
    task_2 = await task_speak(random_word)
    assert task_2 == f"I say, {random_word}!"
