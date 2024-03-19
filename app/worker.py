from typing import Any, List, Optional

from asgi_correlation_id.context import correlation_id
from celery import Celery  # type: ignore
from pydantic import UUID4, AnyHttpUrl
from sentry_sdk import Client
from usp.tree import AbstractSitemap  # type: ignore
from usp.tree import sitemap_tree_for_homepage  # type: ignore

from app.api.monitoring import configure_monitoring
from app.api.utilities import create_or_update_website_page, fetch_pagespeedinsights
from app.core.celery import create_celery_worker
from app.core.config import settings
from app.core.logger import logger
from app.schemas import (
    PageSpeedInsightsDevice,
    WebsiteMapPage,
    WebsiteMapProcessedResult,
    WebsitePageSpeedInsightsBase,
    WebsitePageSpeedInsightsProcessing,
)
from app.schemas.website_pagespeedinsights import PSIDevice

celery_app: Celery = create_celery_worker()
sentry_client: Client | None = configure_monitoring()

if not settings.api.debug:  # pragma: no cover

    @celery_app.before_task_publish.connect()
    def transfer_correlation_id(headers: Any) -> None:
        headers[settings.api.asgi_header_key] = correlation_id.get()

    @celery_app.task_prerun.connect()
    def load_correlation_id(task: Any) -> None:
        id_value: Any = task.request.get(settings.api.asgi_header_key)
        correlation_id.set(id_value)


@celery_app.task(
    name="tasks:task_speak",
    acks_late=True,
)
def task_speak(
    word: str,
) -> str:
    return f"I say, {word}!"


@celery_app.task(
    name="tasks:task_request_to_delete_user",
    acks_late=True,
)
def task_request_to_delete_user(user_id: UUID4) -> None:
    # TODO: Send email to user to confirm deletion
    # TODO: flag user as pending delete.
    logger.info(
        f"User({user_id}) requested to delete their account."
    )  # pragma: no cover


@celery_app.task(
    name="tasks:task_request_to_delete_client",
    acks_late=True,
)
def task_request_to_delete_client(user_id: UUID4, client_id: UUID4) -> None:
    # TODO: Send email to user to confirm deletion
    # TODO: flag client as pending delete.
    logger.info(
        f"User({user_id}) requested to delete the Client({client_id})."
    )  # pragma: no cover


@celery_app.task(
    name="sitemaps:task_website_sitemap_fetch_pages",
    acks_late=True,
)
async def task_website_sitemap_fetch_pages(
    website_id: UUID4,
    sitemap_id: UUID4,
    sitemap_url: AnyHttpUrl,
) -> WebsiteMapProcessedResult:
    logger.info(
        f"Fetching sitemap pages for website_id {website_id} \
            from {sitemap_id} at {sitemap_url}"
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
            sitemap_id=website_id,
            page=sm_page,
        )
    return WebsiteMapProcessedResult(
        url=sitemap.url,
        website_id=website_id,
        sitemap_id=sitemap_id,
    )


@celery_app.task(
    name="webpages:task_website_page_pagespeedinsights_fetch",
    acks_late=True,
)
def task_website_page_pagespeedinsights_fetch(
    website_id: UUID4,
    page_id: UUID4,
    fetch_url: AnyHttpUrl,
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
