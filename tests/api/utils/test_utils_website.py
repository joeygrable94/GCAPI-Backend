from typing import Any
from unittest.mock import patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_domain
from tests.utils.website_maps import create_random_website_map
from tests.utils.websites import create_random_website
from usp.objects.page import SitemapPage  # type: ignore

from app.api.utilities import create_or_update_website_page
from app.schemas.website import WebsiteRead
from app.schemas.website_map import WebsiteMapRead
from app.schemas.website_page import WebsitePageRead

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
    website: WebsiteRead = await create_random_website(db_session)
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    page = SitemapPage(url=page_url, priority=0.5)
    with patch(
        "app.api.utilities.request.urlopen"
    ) as mock_create_or_update_website_page_url_response:
        mock_create_or_update_website_page_url_response.return_value = MockRequestUrlopenResponse()  # type: ignore  # noqa: E501
        output = await create_or_update_website_page(website.id, sitemap.id, page)  # type: ignore  # noqa: E501
        assert isinstance(output, WebsitePageRead)


async def test_create_or_update_website_page_create_then_update(
    db_session: AsyncSession,
) -> None:
    page_url = "https://%s/" % random_domain()
    page_url_b = "https://%s/" % random_domain()
    website: WebsiteRead = await create_random_website(db_session)
    sitemap: WebsiteMapRead = await create_random_website_map(db_session)
    page = SitemapPage(url=page_url, priority=0.5)
    page_b = SitemapPage(url=page_url_b, priority=0.25)
    with patch(
        "app.api.utilities.request.urlopen"
    ) as mock_create_or_update_website_page_url_response:
        mock_create_or_update_website_page_url_response.return_value = MockRequestUrlopenResponse()  # type: ignore  # noqa: E501
        output_a = await create_or_update_website_page(website.id, sitemap.id, page)  # type: ignore  # noqa: E501
        assert isinstance(output_a, WebsitePageRead)
    with patch(
        "app.api.utilities.request.urlopen"
    ) as mock_create_or_update_website_page_url_response:
        mock_create_or_update_website_page_url_response.return_value = MockRequestUrlopenResponse()  # type: ignore  # noqa: E501
        output_b = await create_or_update_website_page(website.id, sitemap.id, page_b)  # type: ignore  # noqa: E501
        assert isinstance(output_b, WebsitePageRead)
