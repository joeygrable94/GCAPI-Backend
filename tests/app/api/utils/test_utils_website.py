from decimal import Decimal
from typing import Any
from unittest.mock import patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utilities import create_or_update_website_page
from app.models import Website
from app.schemas import WebsiteMapPage, WebsiteMapRead, WebsiteRead
from tests.utils.utils import random_domain
from tests.utils.website_maps import create_random_website_map
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


class MockRequestUrlopenResponse:
    def __init__(self) -> None:
        self.status: int = 200

    def getcode(self) -> Any:
        return self.status


async def test_create_or_update_website_page_create(
    db_session: AsyncSession,
) -> None:
    page_url = "https://%s/" % random_domain()
    website: Website | WebsiteRead = await create_random_website(db_session)
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    page = WebsiteMapPage(url=page_url, priority=Decimal(0.5))
    with patch(
        "app.core.utilities.websites.fetch_url_status_code"
    ) as mock_fetch_url_status_code:
        mock_fetch_url_status_code.return_value = 200
        output = await create_or_update_website_page(website.id, sitemap.id, page)
        assert output is None


async def test_create_or_update_website_page_create_then_update(
    db_session: AsyncSession,
) -> None:
    page_url = "https://%s/" % random_domain()
    website: Website | WebsiteRead = await create_random_website(db_session)
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    page = WebsiteMapPage(url=page_url, priority=Decimal(0.5))
    page_b = WebsiteMapPage(url=page_url, priority=Decimal(0.25))
    with patch(
        "app.core.utilities.websites.fetch_url_status_code"
    ) as mock_fetch_url_status_code:
        mock_fetch_url_status_code.return_value = 200
        output_a = await create_or_update_website_page(website.id, sitemap.id, page)
        assert output_a is None
    with patch(
        "app.core.utilities.websites.fetch_url_status_code"
    ) as mock_fetch_url_status_code:
        mock_fetch_url_status_code.return_value = 200
        output_b = await create_or_update_website_page(website.id, sitemap.id, page_b)
        assert output_b is None
        output_c = await create_or_update_website_page(website.id, sitemap.id, page_b)
        assert output_c is None


async def test_create_or_update_website_page_create_and_update(
    db_session: AsyncSession,
) -> None:
    page_url = "https://getcommunity.com/"
    website: Website | WebsiteRead = await create_random_website(db_session)
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    map_page = WebsiteMapPage(url=page_url, priority=Decimal(0.5))
    output_a = await create_or_update_website_page(
        str(website.id), str(sitemap.id), map_page
    )
    assert output_a is None
    output_b = await create_or_update_website_page(
        str(website.id), str(sitemap.id), map_page
    )
    assert output_b is None
