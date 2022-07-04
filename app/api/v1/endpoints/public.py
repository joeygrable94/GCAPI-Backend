from typing import Dict

from fastapi import APIRouter, Depends

from app.core.security import get_current_active_user
from app.db.schemas.user import UserRead

public_router: APIRouter = APIRouter()


@public_router.get("/status")
async def status() -> Dict[str, str]:
    return {"status": "ok"}


# @public_router.get("/")
# async def index(request: Request):
# 	return templates.TemplateResponse("pages/index.html", {"request":request})

@public_router.get("/message")
async def auth_message(user: UserRead = Depends(get_current_active_user)):
	return {"message": f"Hello {user.email}!"}

# from starlette.responses import RedirectResponse
# @app.get("/redirect")
# async def redirect():
#     url = app.url_path_for("redirected")
#     response = RedirectResponse(url=url)
#     return response

# @app.get("/redirected")
# async def redirected():
#     logger.debug("REDIRECTED")
#     return {"message": "you've been redirected"}
