from typing import Any, Dict

from fastapi import APIRouter

from app.api.deps import GetQueryParams

router: APIRouter = APIRouter()


@router.get(
    "/status",
    name="public:status",
    response_model=Dict[str, Any],
)
async def status(query: GetQueryParams) -> Dict[str, Any]:
    """
    Fetches the current API status.
    """
    return {"status": "ok"}
