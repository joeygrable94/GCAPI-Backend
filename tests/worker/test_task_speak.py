import pytest
from tests.utils.utils import random_lower_string

from app.tasks import task_speak


@pytest.mark.anyio
def test_worker_task_speak() -> None:
    random_word = random_lower_string()
    result = task_speak(random_word)
    assert result == f"I say, {random_word}!"
