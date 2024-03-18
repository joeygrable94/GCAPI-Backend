from typing import Any

from celery.result import AsyncResult  # type: ignore
from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, get_current_user
from app.core.security import auth
from app.schemas import TaskState

router: APIRouter = APIRouter()


@router.get(
    "/{task_id}",
    name="tasks:get_status",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_current_user),
    ],
    response_model=TaskState,
)
def get_tasks_status(
    current_user: CurrentUser,
    task_id: Any,
) -> TaskState:  # pragma: no cover
    """Retrieve the status of a task by task_id.

    Permissions:
    ------------
    `role=user` : all tasks

    Returns:
    --------
    `TaskState` : a dictionary containing the worker task id, status,
        and maybe the result

    """
    task_result = AsyncResult(task_id)
    return TaskState(
        task_id=task_id, task_status=task_result.status, task_result=task_result.result
    )
