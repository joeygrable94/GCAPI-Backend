from typing import Any

from pydantic import UUID4, BaseModel


class TaskState(BaseModel):
    task_id: UUID4 | str | Any | None
    task_status: str | Any
    task_result: Any = None
