import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_domain
from tests.utils.websites import create_random_website

from app.api.utilities import create_or_update_website_map
from app.models.website import Website
from app.schemas.website import WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_create_or_update_website_map_create(
    db_session: AsyncSession,
) -> None:
    sitemap_url = "https://%s/sitemap.xml" % random_domain()
    website: Website | WebsiteRead = await create_random_website(db_session)
    output = await create_or_update_website_map(str(website.id), sitemap_url)  # type: ignore  # noqa: E501
    assert output is None


async def test_create_or_update_website_map_create_then_update(
    db_session: AsyncSession,
) -> None:
    sitemap_url = "https://%s/sitemap.xml" % random_domain()
    website: Website | WebsiteRead = await create_random_website(db_session)
    output_a = await create_or_update_website_map(str(website.id), sitemap_url)  # type: ignore  # noqa: E501
    assert output_a is None
    output_b = await create_or_update_website_map(str(website.id), sitemap_url)  # type: ignore  # noqa: E501
    assert output_b is None
