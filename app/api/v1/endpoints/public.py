from typing import Any, Dict

from fastapi import APIRouter, Depends, Request, Response

from app.api.deps import GetQueryParams
from app.core.config import Settings, get_settings
from app.core.security import CsrfProtect
from app.schemas import CsrfToken
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
    if query.speak:
        speak_task = task_speak.delay(query.speak)
        return {"status": "ok", "speak_task_id": speak_task.id}
    return {"status": "ok"}


@router.get(
    "/csrf",
    name="public:csrf",
    dependencies=[
        Depends(CsrfProtect),
        Depends(get_settings),
    ],
    response_model=CsrfToken,
)
async def get_csrf(
    response: Response,
    csrf_protect: CsrfProtect = Depends(),
    setting: Settings = Depends(get_settings),
) -> CsrfToken:
    """Generates an secure CSRF token for the API.

    Permissions:
    ------------
    anyone can access this endpoint

    Returns:
    --------
    `Dict[str, Any]` : a dictionary containing the CSRF token for the API

    """
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens(
        setting.CSRF_SECRET_KEY
    )

    csrf_protect.set_csrf_cookie(signed_token, response)

    return CsrfToken(csrf_token=csrf_token)
