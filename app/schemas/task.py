from enum import Enum
from typing import Any

from pydantic import BaseModel


class TaskStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class TaskState(BaseModel):
    task_id: str
    task_status: TaskStatus = TaskStatus.PENDING
    task_time: float | None = None
    task_result: Any | None = None
