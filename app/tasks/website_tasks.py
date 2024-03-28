import xml.etree.ElementTree as ET
from typing import Optional

from app.api.utilities import (
    create_or_update_website_map,
    create_or_update_website_page,
    create_website_pagespeedinsights,
    fetch_pagespeedinsights,
)
from app.broker import broker
from app.core.logger import logger
from app.core.utilities.websites import (
    check_is_sitemap_index,
    check_is_sitemap_page,
    check_is_sitemap_urlset,
    fetch_url_page_text,
    parse_sitemap_xml,
    process_sitemap_index,
    process_sitemap_page_urlset,
)
from app.schemas import (
    PageSpeedInsightsDevice,
    PSIDevice,
    WebsiteMapProcessedResult,
    WebsitePageSpeedInsightsBase,
    WebsitePageSpeedInsightsProcessing,
)


@broker.task(task_name="sitemaps:task_website_sitemap_process_xml")
async def task_website_sitemap_process_xml(
    website_id: str,
    sitemap_id: str,
    sitemap_url: str,
) -> WebsiteMapProcessedResult:
    sitemap_text: str = await fetch_url_page_text(sitemap_url)
    sitemap_root: ET.Element = await parse_sitemap_xml(sitemap_text)
    # Check if the sitemap is a sitemap index
    if await check_is_sitemap_index(sitemap_root):
        logger.info(
            f"Processing sitemap index for website_id {website_id} from {sitemap_id} at {sitemap_url}"  # noqa: E501
        )
        sitemap_urls = await process_sitemap_index(sitemap_root)
        for sm_url in sitemap_urls:
            await create_or_update_website_map(website_id, sm_url)
        logger.info(f"Discovered {len(sitemap_urls)} sitemap pages")
    # Check if the sitemap is a sitemap page
    elif await check_is_sitemap_page(sitemap_root) or await check_is_sitemap_urlset(
        sitemap_root
    ):
        logger.info(
            f"Processing sitemap urlset for website_id {website_id} from {sitemap_id} at {sitemap_url}"  # noqa: E501
        )
        sitemap_webpages = await process_sitemap_page_urlset(sitemap_root)
        for sm_page in sitemap_webpages:
            await create_or_update_website_page(website_id, sitemap_id, page=sm_page)
        logger.info(f"Processed {len(sitemap_webpages)} sitemap website page urls")
    return WebsiteMapProcessedResult(
        url=sitemap_url,
        website_id=website_id,
        sitemap_id=sitemap_id,
    )


@broker.task(task_name="webpages:task_website_page_pagespeedinsights_fetch")
async def task_website_page_pagespeedinsights_fetch(
    website_id: str,
    page_id: str,
    fetch_url: str,
    device: PSIDevice,
) -> WebsitePageSpeedInsightsProcessing:
    logger.info(
        f"Fetching PageSpeedInsights for website {website_id}, \
            page {page_id}, URL[{fetch_url}]"
    )
    is_created: bool = False
    insights: Optional[WebsitePageSpeedInsightsBase] = fetch_pagespeedinsights(
        fetch_url=fetch_url,
        device=PageSpeedInsightsDevice(device=device),
    )
    if insights is not None:
        await create_website_pagespeedinsights(
            website_id=website_id,
            page_id=page_id,
            insights=insights,
        )
        is_created = True
    return WebsitePageSpeedInsightsProcessing(
        website_id=website_id,
        page_id=page_id,
        insights=insights,
        is_created=is_created,
    )
