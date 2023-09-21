from fastapi import APIRouter

from app.api.v1.endpoints import (
    clients,
    public,
    tasks,
    users,
    web_pages,
    web_pagespeedinsights,
    web_sitemaps,
    websites,
)

router_v1 = APIRouter()


# public routes
router_v1.include_router(
    public.router,
    tags=["Public"],
)

# task routes
router_v1.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["Tasks"],
)

# client routes
router_v1.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

# client routes
router_v1.include_router(
    clients.router,
    prefix="/clients",
    tags=["Clients"],
)

# website routes
router_v1.include_router(
    websites.router,
    prefix="/websites",
    tags=["Websites"],
)

# website page routes
router_v1.include_router(
    web_pages.router,
    prefix="/webpages",
    tags=["Website Pages"],
)

# website sitemap routes
router_v1.include_router(
    web_sitemaps.router,
    prefix="/sitemaps",
    tags=["Website Sitemaps"],
)

# website page speed insights routes
router_v1.include_router(
    web_pagespeedinsights.router,
    prefix="/psi",
    tags=["Website Page Speed Insights"],
)
