from typing import Any

from pydantic import UUID4, BaseModel


class TaskState(BaseModel):
    task_id: UUID4
    task_status: str
    task_result: Any
