from typing import Any, Dict

from fastapi import APIRouter

from app.api.deps import GetQueryParams

router: APIRouter = APIRouter()


@router.get("/status")
async def status(query: GetQueryParams) -> Dict[str, Any]:
    """
    Fetches the current API status.
    """
    return {"status": "ok"}
