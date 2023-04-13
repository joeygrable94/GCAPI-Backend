from unittest.mock import patch

import pytest
from pydantic import AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.websites import create_random_website

from app.api.utils import save_sitemap_pages
from app.schemas import WebsiteMapPage, WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_save_sitemap_pages(db_session: AsyncSession) -> None:
    website: WebsiteRead = await create_random_website(db_session)
    sitemap_url: AnyHttpUrl = "https://getcommunity.com/"  # type: ignore
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

    with patch(
        "app.api.utils.create_or_update_website_page"
    ) as mock_create_or_update_website_page:
        mock_create_or_update_website_page.return_value = None
        sitemap_id = await save_sitemap_pages(website.id, sitemap_url, sitemap_pages)
        assert sitemap_id
