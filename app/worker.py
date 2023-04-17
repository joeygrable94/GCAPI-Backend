import asyncio
from typing import Any, Dict, List, Optional

from asgi_correlation_id.context import correlation_id
from pydantic import UUID4, AnyHttpUrl
from raven import Client  # type: ignore
from usp.tree import AbstractSitemap  # type: ignore
from usp.tree import sitemap_tree_for_homepage
from asgiref.sync import async_to_sync

from app.api.utils import fetch_pagespeedinsights, save_sitemap_pages
from app.core.celery import celery_app
from app.core.config import settings
from app.core.logger import logger
from app.schemas import (
    PageSpeedInsightsDevice,
    WebsiteMapPage,
    WebsiteMapProcessing,
    WebsitePageSpeedInsightsBase,
    WebsitePageSpeedInsightsProcessing,
)

if not settings.DEBUG_MODE:  # pragma: no cover
    if settings.SENTRY_DSN:
        client_sentry: Client = Client(settings.SENTRY_DSN)

    @celery_app.before_task_publish.connect()
    def transfer_correlation_id(headers: Any) -> None:
        headers[settings.ASGI_ID_HEADER_KEY] = correlation_id.get()

    @celery_app.task_prerun.connect()
    def load_correlation_id(task: Any) -> None:
        id_value: Any = task.request.get(settings.ASGI_ID_HEADER_KEY)
        correlation_id.set(id_value)


@celery_app.task(acks_late=True)
def task_speak(word: str) -> str:
    return f"I say, {word}!"


@celery_app.task(acks_late=True)
def task_website_sitemap_fetch_pages(
    website_id: UUID4,
    sitemap_url: AnyHttpUrl,
) -> Dict[str, Any]:
    logger.info(f"Fetching sitemap pages for website_id {website_id}")
    sitemap: AbstractSitemap = sitemap_tree_for_homepage(sitemap_url)
    # sitemap_pages: List[WebsiteMapPage] = []
    sitemap_pages: List[Dict[str, Any]] = []
    for pg in sitemap.all_pages():
        sitemap_pages.append(
            WebsiteMapPage(
                url=pg.url,
                priority=pg.priority,
                last_modified=pg.last_modified,
                change_frequency=pg.change_frequency,
                news_story=pg.news_story,
            ).dict()
        )
    sitemap_processing = task_website_sitemap_process_pages.delay(
        website_id, sitemap.url, sitemap_pages
    )
    return WebsiteMapProcessing(
        url=sitemap.url,
        website_id=website_id,
        task_id=sitemap_processing.id,
    ).dict()


@celery_app.task(acks_late=True)
def task_website_sitemap_process_pages(
    website_id: UUID4,
    sitemap_url: AnyHttpUrl,
    sitemap_pages: List[WebsiteMapPage],
) -> None:
    asyncio.run(save_sitemap_pages(website_id, sitemap_url, sitemap_pages))


@celery_app.task(acks_late=True)
def task_website_page_pagespeedinsights_fetch(
    website_id: UUID4,
    page_id: UUID4,
    fetch_url: AnyHttpUrl,
    device: str,
) -> Dict[str, Any]:
    logger.info(
        f"Fetching PageSpeedInsights for website {website_id}, page {page_id}, URL[{fetch_url}]"
    )
    insights: Optional[WebsitePageSpeedInsightsBase] = fetch_pagespeedinsights(
        fetch_url=fetch_url,
        device=PageSpeedInsightsDevice(device=device),
    )
    return WebsitePageSpeedInsightsProcessing(
        website_id=website_id,
        page_id=page_id,
        insights=insights,
    ).dict()
