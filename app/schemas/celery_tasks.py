from typing import Any

from pydantic import BaseModel


class TaskState(BaseModel):
    task_id: Any
    task_status: Any
    task_result: Any
