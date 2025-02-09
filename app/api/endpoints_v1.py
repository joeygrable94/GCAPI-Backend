from fastapi import APIRouter, Depends

from app.entities.core_organization.router import router as organization_router
from app.entities.core_user.router import router as users_router
from app.entities.go_property.router import router as go_property_router
from app.entities.platform.router import router as platform_router
from app.entities.public.router import router as public_router
from app.entities.security.router import router as security_router
from app.entities.tracking_link.router import router as tracking_links_router
from app.entities.website.router import router as websites_router
from app.entities.website_keywordcorpus.router import router as web_keywordcorpus_router
from app.entities.website_page.router import router as web_pages_router
from app.entities.website_pagespeedinsight.router import (
    router as web_pagespeedinsights_router,
)
from app.services.auth0 import auth_controller

router_v1 = APIRouter(
    prefix="/v1", dependencies=[Depends(auth_controller.implicit_scheme)]
)


# Public routes
router_v1.include_router(
    public_router,
    tags=["Public"],
)

router_v1.include_router(
    security_router,
    tags=["Security"],
)

# User routes
router_v1.include_router(
    users_router,
    prefix="/users",
    tags=["Users"],
)

# Organization routes
router_v1.include_router(
    organization_router,
    prefix="/organizations",
    tags=["Organizations"],
)

# Platforms routes
router_v1.include_router(
    platform_router,
    prefix="/platforms",
    tags=["Platforms"],
)

# Tracking Links routes
router_v1.include_router(
    tracking_links_router,
    prefix="/utmlinks",
    tags=["Tracking Links"],
)

# Google Properties routes
router_v1.include_router(
    go_property_router,
    prefix="/go",
    tags=["Google Properties"],
)

# website routes
router_v1.include_router(
    websites_router,
    prefix="/websites",
    tags=["Websites"],
)

# website page routes
router_v1.include_router(
    web_pages_router,
    prefix="/webpages",
    tags=["Website Pages"],
)

# website page speed insights routes
router_v1.include_router(
    web_pagespeedinsights_router,
    prefix="/psi",
    tags=["Website Page Speed Insights"],
)

# website page keyword corpus routes
router_v1.include_router(
    web_keywordcorpus_router,
    prefix="/kwc",
    tags=["Website Page Keyword Corpus"],
)
