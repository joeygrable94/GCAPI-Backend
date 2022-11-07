from fastapi import APIRouter

from app.api.v1.endpoints import auth, public, users

router_v1 = APIRouter()


# public routes
router_v1.include_router(public.router, tags=["public"])

# auth routes
router_v1.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)

# users routes
router_v1.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)
