from fastapi import APIRouter

from app.api.v1.endpoints import (
    bdx_feed,
    clients,
    go_a4_property,
    go_a4_stream,
    go_cloud,
    go_sc_metrics,
    go_sc_property,
    notes,
    public,
    security,
    sharpspring,
    tasks,
    users,
    web_keywordcorpus,
    web_pages,
    web_pagespeedinsights,
    web_sitemaps,
    websites,
)

router_v1 = APIRouter(prefix="/v1")


# Public routes
router_v1.include_router(
    public.router,
    tags=["Public"],
)

router_v1.include_router(
    security.router,
    tags=["Security"],
)

# Task routes
router_v1.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["Tasks"],
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

# Note routes
router_v1.include_router(
    notes.router,
    prefix="/notes",
    tags=["Notes"],
)

# Bdx Feed routes
router_v1.include_router(
    bdx_feed.router,
    prefix="/bdx",
    tags=["BDX Feeds"],
)

# Sharpspring routes
router_v1.include_router(
    sharpspring.router,
    prefix="/sharpspring",
    tags=["SharpSpring Accounts"],
)

# Google Cloud routes
router_v1.include_router(
    go_cloud.router,
    prefix="/go/cloud",
    tags=["Google Cloud Accounts"],
)

# GA4 routes
router_v1.include_router(
    go_a4_property.router,
    prefix="/ga4/property",
    tags=["Google Analytics 4 Properties"],
)

router_v1.include_router(
    go_a4_stream.router,
    prefix="/ga4/stream",
    tags=["Google Analytics 4 Property Streams"],
)

# GSC routes
router_v1.include_router(
    go_sc_property.router,
    prefix="/go/search/property",
    tags=["Google Search Console Properties"],
)

router_v1.include_router(
    go_sc_metrics.router,
    prefix="/go/search/metric",
    tags=["Google Search Console Property Metrics"],
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
