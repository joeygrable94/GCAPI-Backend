from typing import List, Optional

# from pydantic import UUID4, AnyHttpUrl
from usp.tree import AbstractSitemap  # type: ignore
from usp.tree import sitemap_tree_for_homepage  # type: ignore

from app.api.utilities import create_or_update_website_page, fetch_pagespeedinsights
from app.broker import broker
from app.core.logger import logger
from app.schemas import (
    PageSpeedInsightsDevice,
    PSIDevice,
    WebsiteMapPage,
    WebsiteMapProcessedResult,
    WebsitePageSpeedInsightsBase,
    WebsitePageSpeedInsightsProcessing,
)


@broker.task(task_name="sitemaps:task_website_sitemap_fetch_pages")
async def task_website_sitemap_fetch_pages(
    website_id: str,
    sitemap_id: str,
    sitemap_url: str,
) -> WebsiteMapProcessedResult:
    logger.info(
        f"Fetching sitemap pages for website_id {website_id} from {sitemap_id} at {sitemap_url}"  # noqa: E501
    )
    sitemap: AbstractSitemap = sitemap_tree_for_homepage(sitemap_url)
    sitemap_pages: List[WebsiteMapPage] = []
    for pg in sitemap.all_pages():
        sitemap_pages.append(
            WebsiteMapPage(
                url=pg.url, priority=pg.priority, last_modified=pg.last_modified
            )
        )
    for sm_page in sitemap_pages:
        await create_or_update_website_page(
            website_id=website_id,
            sitemap_id=sitemap_id,
            page=sm_page,
        )
    return WebsiteMapProcessedResult(
        url=sitemap.url,
        website_id=website_id,
        sitemap_id=sitemap_id,
    )


@broker.task(task_name="webpages:task_website_page_pagespeedinsights_fetch")
def task_website_page_pagespeedinsights_fetch(
    website_id: str,
    page_id: str,
    fetch_url: str,
    device: PSIDevice,
) -> WebsitePageSpeedInsightsProcessing:
    logger.info(
        f"Fetching PageSpeedInsights for website {website_id}, \
            page {page_id}, URL[{fetch_url}]"
    )
    insights: Optional[WebsitePageSpeedInsightsBase] = fetch_pagespeedinsights(
        fetch_url=fetch_url,
        device=PageSpeedInsightsDevice(device=device),
    )
    return WebsitePageSpeedInsightsProcessing(
        website_id=website_id,
        page_id=page_id,
        insights=insights,
    )
