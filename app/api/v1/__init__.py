from fastapi import APIRouter

from app.api.v1.endpoints import (
    clients,
    notes,
    public,
    security,
    tasks,
    users,
    web_keywordcorpus,
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

router_v1.include_router(
    security.router,
    tags=["Security"],
)

# task routes
router_v1.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["Tasks"],
)

# user routes
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

# note routes
router_v1.include_router(
    notes.router,
    prefix="/notes",
    tags=["Notes"],
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

# website page keyword corpus routes
router_v1.include_router(
    web_keywordcorpus.router,
    prefix="/kwc",
    tags=["Website Page Keyword Corpus"],
)
