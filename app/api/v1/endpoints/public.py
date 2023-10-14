from typing import Any, Dict

from fastapi import APIRouter, Request

from app.api.deps import GetQueryParams
from app.worker import task_speak

router: APIRouter = APIRouter()


@router.get(
    "/status",
    name="public:status",
    response_model=Dict[str, Any],
)
async def status(
    request: Request,
    query: GetQueryParams,
) -> Dict[str, Any]:
    """Retrieve the status of the API.

    Permissions:
    ------------
    anyone can access this endpoint

    Returns:
    --------
    `Dict[str, Any]` : a dictionary containing the status of the API

    """
    if query.message:
        speak_task = task_speak.delay(query.message)
        return {"status": "ok", "speak_task_id": speak_task.id}
    return {"status": "ok"}
