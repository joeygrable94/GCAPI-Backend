from fastapi import APIRouter

from app.api.v1.endpoints import public

router_v1 = APIRouter()


# public routes
router_v1.include_router(public.router, tags=["public"])

# # auth routes
# router_v1.include_router(
#     oauth.router,
#     prefix="/auth",
#     tags=["auth"],
# )
