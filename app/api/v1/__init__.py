from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    clients,
    items,
    public,
    users,
    websites
)


router_v1 = APIRouter()


# public routes
router_v1.include_router(
    public.router,
    tags=["public"]
)

# auth routes
router_v1.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)

# user routes
router_v1.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)

# item routes
router_v1.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
)

# client routes
router_v1.include_router(
    clients.router,
    prefix="/clients",
    tags=["clients"]
)

# website routes
router_v1.include_router(
    websites.router,
    prefix="/websites",
    tags=["websites"]
)
