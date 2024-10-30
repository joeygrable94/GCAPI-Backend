from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.api.deps import (
    GetPublicQueryParams,
    PermissionController,
    PublicQueryParams,
    get_async_db,
    get_current_user,
    get_permission_controller,
)
from app.core.security import auth

router: APIRouter = APIRouter()


@router.get(
    "/status",
    name="public:status",
    dependencies=[
        Depends(PublicQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Dict[str, Any],
)
async def status(
    query: GetPublicQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Dict[str, Any]:
    """Retrieve the status of the API.

    Permissions:
    ------------
    anyone can access this endpoint

    Returns:
    --------
    `Dict[str, Any]` : a dictionary containing the status of the API

    """
    return {"status": "ok"}
