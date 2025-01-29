from fastapi import APIRouter, Depends

from app.api.v1.endpoints import (
    clients,
    go_property,
    platform,
    public,
    security,
    tracking_links,
    users,
    web_keywordcorpus,
    web_pages,
    web_pagespeedinsights,
    web_sitemaps,
    websites,
)
from app.core.security import auth

router_v1 = APIRouter(prefix="/v1", dependencies=[Depends(auth.implicit_scheme)])


# Public routes
router_v1.include_router(
    public.router,
    tags=["Public"],
)

router_v1.include_router(
    security.router,
    tags=["Security"],
)

# User routes
router_v1.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

# Client routes
router_v1.include_router(
    clients.router,
    prefix="/clients",
    tags=["Clients"],
)

# Platforms routes
router_v1.include_router(
    platform.router,
    prefix="/platforms",
    tags=["Platforms"],
)

# Tracking Links routes
router_v1.include_router(
    tracking_links.router,
    prefix="/utmlinks",
    tags=["Tracking Links"],
)

# Google Properties routes
router_v1.include_router(
    go_property.router,
    prefix="/go",
    tags=["Google Properties"],
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
