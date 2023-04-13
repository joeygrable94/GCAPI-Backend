from celery.result import AsyncResult  # type: ignore
from fastapi import APIRouter, Depends
from pydantic import UUID4

from app.api.deps import CurrentUser
from app.core.auth import auth
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
    task_id: UUID4,
) -> TaskState:  # pragma: no cover
    task_result = AsyncResult(task_id)
    return TaskState(
        task_id=task_id, task_status=task_result.status, task_result=task_result.result
    )
