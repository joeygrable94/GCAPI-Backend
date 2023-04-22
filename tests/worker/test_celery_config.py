import pytest
from typing import Any, Dict
from app.worker.celery import route_task


def test_route_task():
    # Test when name has a queue specified
    name: str = "queue1:task1"
    args: str = "arg1"
    kwargs: Dict[str, str] = {"key1": "value1"}
    options: Dict[Any, Any] = {}
    expected_result: Dict[str, str] = {"queue": "queue1"}
    assert route_task(name, args, kwargs, options) == expected_result

    # Test when name has no queue specified
    name: str = "task2"
    args: str = "arg2"
    kwargs: Dict[str, str] = {"key2": "value2"}
    options: Dict[Any, Any] = {}
    expected_result: Dict[str, str] = {"queue": "tasks"}
    assert route_task(name, args, kwargs, options) == expected_result
