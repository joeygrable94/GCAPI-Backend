from typing import Any
from typing import Dict

from app.core.celery import route_task


def test_route_task() -> None:
    # Test when name has a queue specified
    name = "queue1:task1"
    args = "arg1"
    kwargs = {"key1": "value1"}
    options: Dict[str, Any] = {}
    expected_result = {"queue": "queue1"}
    assert route_task(name, args, kwargs, options) == expected_result

    # Test when name has no queue specified
    name = "task2"
    args = "arg2"
    kwargs = {"key2": "value2"}
    options: Dict[str, Any] = {}
    expected_result = {"queue": "tasks"}
    assert route_task(name, args, kwargs, options) == expected_result
