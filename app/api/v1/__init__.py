from fastapi import APIRouter

from app.api.v1.endpoints import auth, clients, public, users, websites

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

# clients routes
router_v1.include_router(
    clients.router,
    prefix="/clients",
    tags=["clients"],
)

# websites routes
router_v1.include_router(
    websites.router,
    prefix="/websites",
    tags=["websites"],
)
