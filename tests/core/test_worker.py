from typing import Any

from tests.utils.utils import random_lower_string
from app.worker import task_speak


def test_celery_task_speak(celery_worker: Any) -> None:
    random_word = random_lower_string()
    result = task_speak(word=random_word)
    assert result == f"I say, {random_word}!"
