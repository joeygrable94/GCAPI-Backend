from typing import Any, Dict

from fastapi import APIRouter, Depends
from taskiq import AsyncTaskiqTask

from app.api.deps import GetPublicQueryParams
from app.core.security.rate_limiter.deps import RateLimiter
from app.tasks import task_speak

router: APIRouter = APIRouter()


@router.get(
    "/status",
    name="public:status",
    dependencies=[Depends(RateLimiter(times=1, seconds=5))],
    response_model=Dict[str, Any],
)
async def status(query: GetPublicQueryParams) -> Dict[str, Any]:
    """Retrieve the status of the API.

    Permissions:
    ------------
    anyone can access this endpoint

    Returns:
    --------
    `Dict[str, Any]` : a dictionary containing the status of the API

    """
    if query.message:
        speak_task: AsyncTaskiqTask = await task_speak.kiq(query.message)
        return {"status": "ok", "speak_task_id": speak_task.task_id}
    return {"status": "ok"}


@router.get(
    "/rate-limited-multiple",
    name="public:rate_limited_multiple",
    dependencies=[
        Depends(RateLimiter(times=1, seconds=5)),
        Depends(RateLimiter(times=2, seconds=15)),
    ],
    response_model=Dict[str, Any],
)
async def rate_limited_multiple(query: GetPublicQueryParams) -> Dict[str, Any]:
    return {"status": "ok"}
