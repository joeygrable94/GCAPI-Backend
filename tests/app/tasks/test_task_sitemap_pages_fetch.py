import unittest.mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.tasks.background import bg_task_website_sitemap_process_xml
from app.utilities.uuids import get_uuid

pytestmark = pytest.mark.asyncio


async def test_task_website_sitemap_process_xml_index_invalid_uuid(
    mock_fetch_sitemap_index: str,
    db_session: AsyncSession,
) -> None:
    website_id = get_uuid()
    invalid_sitemap_id = "invalid-sitemap-id"
    sitemap_url = "https://getcommunity.com/sitemap.xml"
    with unittest.mock.patch(
        "app.entities.website_sitemap.utilities.fetch_url_page_text"
    ) as mock_fetch_url_page_text:
        mock_fetch_url_page_text.return_value = mock_fetch_sitemap_index
        await bg_task_website_sitemap_process_xml(
            str(website_id), str(invalid_sitemap_id), sitemap_url
        )


async def test_task_website_sitemap_process_xml_index(
    mock_fetch_sitemap_index: str,
    db_session: AsyncSession,
) -> None:
    website_id = get_uuid()
    sitemap_id = get_uuid()
    sitemap_url = "https://getcommunity.com/sitemap.xml"
    with unittest.mock.patch(
        "app.entities.website_sitemap.utilities.fetch_url_page_text"
    ) as mock_fetch_url_page_text:
        mock_fetch_url_page_text.return_value = mock_fetch_sitemap_index
        await bg_task_website_sitemap_process_xml(
            str(website_id), str(sitemap_id), sitemap_url
        )


async def test_task_website_sitemap_process_xml_page(
    mock_fetch_sitemap_page: str,
    db_session: AsyncSession,
) -> None:
    website_id = get_uuid()
    sitemap_id = get_uuid()
    sitemap_url = "https://getcommunity.com/branch-sitemap.xml"
    with unittest.mock.patch(
        "app.entities.website_sitemap.utilities.fetch_url_page_text"
    ) as mock_fetch_url_page_text:
        mock_fetch_url_page_text.return_value = mock_fetch_sitemap_page
        with unittest.mock.patch(
            "app.entities.website_sitemap.utilities.fetch_url_status_code"
        ) as mock_fetch_url_page_status_code:
            mock_fetch_url_page_status_code.return_value = 200
            await bg_task_website_sitemap_process_xml(
                str(website_id), str(sitemap_id), sitemap_url
            )
