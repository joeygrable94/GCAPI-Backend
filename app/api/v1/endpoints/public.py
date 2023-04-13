from typing import Any, Dict

from fastapi import APIRouter

from app.api.deps import GetQueryParams
from app.worker import task_speak

router: APIRouter = APIRouter()


@router.get(
    "/status",
    name="public:status",
    response_model=Dict[str, Any],
)
async def status(query: GetQueryParams) -> Dict[str, Any]:
    if query.speak:
        speak_task = task_speak.delay(query.speak)
        return {"status": "ok", "speak_task_id": speak_task.id}
    return {"status": "ok"}
