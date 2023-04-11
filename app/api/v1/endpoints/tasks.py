from typing import Any

from celery.result import AsyncResult  # type: ignore
from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, GetQueryParams
from app.core.auth import auth
from app.schemas import TaskState

router: APIRouter = APIRouter()


@router.get(
    "/{task_id}",
    name="tasks:get_status",
    dependencies=[Depends(auth.implicit_scheme)],
    response_model=TaskState,
)
def get_status(
    current_user: CurrentUser,
    query: GetQueryParams,
    task_id: Any,
) -> TaskState:
    task_result = AsyncResult(task_id)
    return TaskState(
        task_id=task_id, task_status=task_result.status, task_result=task_result.result
    )
