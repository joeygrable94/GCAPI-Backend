from typing import Any

from celery.result import AsyncResult  # type: ignore
from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser
from app.core.security import auth
from app.schemas import TaskState

router: APIRouter = APIRouter()


@router.get(
    "/{task_id}",
    name="tasks:get_status",
    dependencies=[Depends(auth.implicit_scheme)],
    response_model=TaskState,
)
def get_tasks_status(
    current_user: CurrentUser,
    task_id: Any,
) -> TaskState:  # pragma: no cover
    """Retrieve the status of a task by task_id.

    Permissions:
    ------------
    `role=admin|manager` : all tasks

    `role=user` : only tasks associated with the user via other models

    Returns:
    --------
    `TaskState` : a dictionary containing the worker task id, status,
        and maybe the result

    """
    task_result = AsyncResult(task_id)
    return TaskState(
        task_id=task_id, task_status=task_result.status, task_result=task_result.result
    )
