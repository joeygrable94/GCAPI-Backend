from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.core.security import get_current_active_user
from app.db.schemas import UserRead

router: APIRouter = APIRouter()


@router.get("/status")
async def status() -> Dict[str, str]:
    return {"status": "ok"}


# @router.get("/")
# async def index(request: Request):
# 	return templates.TemplateResponse("pages/index.html", {"request":request})


@router.get("/message")
async def auth_message(user: UserRead = Depends(get_current_active_user)) -> Any:
    return {"message": f"Hello {user.email}!"}


# from starlette.responses import RedirectResponse
# @router.get("/redirect")
# async def redirect():
#     url = app.url_path_for("redirected")
#     response = RedirectResponse(url=url)
#     return response

# @router.get("/redirected")
# async def redirected():
#     logger.debug("REDIRECTED")
#     return {"message": "you've been redirected"}
