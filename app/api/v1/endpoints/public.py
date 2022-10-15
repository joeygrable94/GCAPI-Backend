from typing import Any, Dict

from fastapi import APIRouter

router: APIRouter = APIRouter()


@router.get("/status")
async def status() -> Dict[str, Any]:
    """
    Fetches the current API status.
    """
    return {"status": "ok"}
