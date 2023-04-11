from typing import Any

import pytest
from tests.utils.utils import random_lower_string

from app.worker import task_speak


@pytest.mark.celery
def test_celery_task_speak(celery_worker: Any) -> None:
    random_word = random_lower_string()
    result = task_speak(random_word)
    assert result == f"I say, {random_word}!"
