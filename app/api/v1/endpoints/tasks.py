from typing import Any, Dict

from fastapi import APIRouter
from celery.result import AsyncResult
from pydantic import BaseModel

from app.db.schemas.user import UserPrincipals
from app.security import Permission, get_current_active_user

router: APIRouter = APIRouter()


class TaskState(BaseModel):
    task_id: Any
    task_status: Any
    task_result: Any


@router.get(
    "/{task_id}",
    response_model=TaskState,
)
def get_status(
    task_id: Any,
    current_user: UserPrincipals = Permission("list", get_current_active_user),
) -> Dict[str, Any]:
    task_result = AsyncResult(task_id)
    return TaskState(
        task_id=task_id,
        task_status=task_result.status,
        task_result=task_result.result
    )
