from fastapi import APIRouter

public_router = APIRouter()

@public_router.get("/status")
async def status():
    return {"status": "ok"}

# @public_router.get("/")
# async def index(request: Request):
# 	return templates.TemplateResponse("pages/index.html", {"request":request})

# @app.get("/authenticated-route")
# async def authenticated_route(user: UserInDB = Depends(current_active_user)):
# 	return {"message": f"Hello {user.email}!"}

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
