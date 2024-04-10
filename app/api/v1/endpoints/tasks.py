from typing import Any

from fastapi import APIRouter, Depends
from taskiq import AsyncTaskiqTask, TaskiqResult
from taskiq_redis.exceptions import ResultIsMissingError

from app.api.deps import CurrentUser, get_current_user
from app.core.security import auth
from app.schemas import TaskState
from app.schemas.task import TaskStatus
from app.worker import task_broker

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
async def get_tasks_status(
    current_user: CurrentUser,
    task_id: str,
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
    task_status: TaskStatus = TaskStatus.PENDING
    task_result: TaskiqResult[Any] | None = None
    task_return_value: Any | None = None
    task_execution_time: float = 0.0
    try:
        task = AsyncTaskiqTask(task_id, result_backend=task_broker.result_backend)
        task_result = await task.get_result()
        if task_result is None:
            raise ResultIsMissingError()
        if task_result.is_err:
            task_status = TaskStatus.ERROR
        if task_result.return_value is not None:
            task_status = TaskStatus.SUCCESS
        task_execution_time = task_result.execution_time
        task_return_value = task_result.return_value
    except ResultIsMissingError:
        task_status = TaskStatus.PENDING
    finally:
        return TaskState(
            task_id=task_id,
            task_status=task_status,
            task_time=task_execution_time,
            task_result=task_return_value,
        )
