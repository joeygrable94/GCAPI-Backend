import asyncio
from typing import Any, Tuple

from asgi_correlation_id.context import correlation_id
from pydantic import UUID4, AnyHttpUrl
from raven import Client  # type: ignore
from usp.tree import AbstractSitemap  # type: ignore
from usp.tree import sitemap_tree_for_homepage

from app.api.utils import fetch_pagespeedinsights, save_sitemap_pages
from app.core.celery import celery_app
from app.core.config import settings
from app.core.logger import logger
from app.schemas import PageSpeedInsightsDevice, WebsitePageSpeedInsightsBase

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
def task_website_sitemap_fetch_url(website_id: UUID4, sitemap_url: AnyHttpUrl) -> AbstractSitemap:
    logger.info(f"Fetching sitemap for website_id {website_id}")
    sitemap: AbstractSitemap = sitemap_tree_for_homepage(sitemap_url)
    return sitemap


@celery_app.task(acks_late=True)
async def task_website_sitemap_process_pages(website_id: UUID4, sitemap: AbstractSitemap) -> None:
    logger.info(f"Processing sitemap for website_id {website_id}")
    await save_sitemap_pages(website_id, sitemap)


@celery_app.task(acks_late=True)
async def task_website_page_pagespeedinsights_fetch(
    website_id: UUID4,
    page_id: UUID4,
    fetch_psi_url: AnyHttpUrl,
    device: str,
) -> Tuple[UUID4, UUID4, WebsitePageSpeedInsightsBase]:
    logger.info(f"Fetching PageSpeedInsights for website {website_id}, page {page_id}")
    insights: WebsitePageSpeedInsightsBase = await fetch_pagespeedinsights(
        fetch_url=fetch_psi_url,
        device=PageSpeedInsightsDevice(device=device),
    )
    return website_id, page_id, insights
