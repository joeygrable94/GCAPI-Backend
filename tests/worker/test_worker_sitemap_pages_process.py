from typing import Any
import unittest.mock
from uuid import UUID
from pydantic import UUID4

import pytest

from app.core.utilities.uuids import get_uuid
from app.schemas.website_map import WebsiteMapPage
from app.worker import task_website_sitemap_process_pages


@pytest.mark.celery
@pytest.mark.asyncio
async def test_task_website_sitemap_process_pages() -> None:
    website_id = get_uuid()
    sitemap_url = "https://getcommunity.com/"
    sitemap_pages = [
        WebsiteMapPage(
            url="https://getcommunity.com/products/",
            priority=0.8,
            last_modified="2022-10-24 15:00:00+00:00",
        ),
        WebsiteMapPage(
            url="https://getcommunity.com/products/gc-video/",
            priority=0.8,
            last_modified="2022-10-24 15:00:00+00:00",
        ),
        WebsiteMapPage(
            url="https://getcommunity.com/products/media/",
            priority=0.8,
            last_modified="2022-10-24 15:00:00+00:00",
        ),
        WebsiteMapPage(
            url="https://getcommunity.com/products/gc-text/",
            priority=0.8,
            last_modified="2022-10-24 15:00:00+00:00",
        ),
    ]

    with unittest.mock.patch(
        "app.worker.save_sitemap_pages"
    ) as mock_save_sitemap_pages:
        mock_save_sitemap_pages.return_value = None

        sitemap_task = task_website_sitemap_process_pages(
            website_id, sitemap_url, sitemap_pages
        )

        assert sitemap_task is None

        mock_save_sitemap_pages.assert_called_once_with(
            website_id, sitemap_url, sitemap_pages
        )
