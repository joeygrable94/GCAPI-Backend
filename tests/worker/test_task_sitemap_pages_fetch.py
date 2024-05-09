import unittest.mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utilities.uuids import get_uuid
from app.schemas import WebsiteMapProcessedResult
from app.tasks import task_website_sitemap_process_xml

pytestmark = pytest.mark.asyncio


async def test_task_website_sitemap_process_xml_index_invalid_uuid(
    mock_fetch_sitemap_index: str,
    db_session: AsyncSession,
) -> None:
    website_id = get_uuid()
    invalid_sitemap_id = "invalid-sitemap-id"
    sitemap_url = "https://getcommunity.com/sitemap.xml"
    with unittest.mock.patch(
        "app.tasks.website_tasks.fetch_url_page_text"
    ) as mock_fetch_url_page_text:
        mock_fetch_url_page_text.return_value = mock_fetch_sitemap_index
        sitemap_task: WebsiteMapProcessedResult = (
            await task_website_sitemap_process_xml(
                str(website_id), str(invalid_sitemap_id), sitemap_url
            )
        )
        assert sitemap_task.url == sitemap_url
        assert sitemap_task.is_active is False
        assert sitemap_task.website_id is None
        assert sitemap_task.sitemap_id is None


async def test_task_website_sitemap_process_xml_index(
    mock_fetch_sitemap_index: str,
    db_session: AsyncSession,
) -> None:
    website_id = get_uuid()
    sitemap_id = get_uuid()
    sitemap_url = "https://getcommunity.com/sitemap.xml"
    with unittest.mock.patch(
        "app.tasks.website_tasks.fetch_url_page_text"
    ) as mock_fetch_url_page_text:
        mock_fetch_url_page_text.return_value = mock_fetch_sitemap_index
        sitemap_task: WebsiteMapProcessedResult = (
            await task_website_sitemap_process_xml(
                str(website_id), str(sitemap_id), sitemap_url
            )
        )
        assert sitemap_task.url == sitemap_url
        assert sitemap_task.website_id == website_id
        assert sitemap_task.sitemap_id == sitemap_id
        assert sitemap_task.is_active is True


async def test_task_website_sitemap_process_xml_page(
    mock_fetch_sitemap_page: str,
    db_session: AsyncSession,
) -> None:
    website_id = get_uuid()
    sitemap_id = get_uuid()
    sitemap_url = "https://getcommunity.com/branch-sitemap.xml"
    with unittest.mock.patch(
        "app.tasks.website_tasks.fetch_url_page_text"
    ) as mock_fetch_url_page_text:
        mock_fetch_url_page_text.return_value = mock_fetch_sitemap_page
        with unittest.mock.patch(
            "app.core.utilities.fetch_url_status_code"
        ) as mock_fetch_url_page_status_code:
            mock_fetch_url_page_status_code.return_value = 200
            sitemap_task: WebsiteMapProcessedResult = (
                await task_website_sitemap_process_xml(
                    str(website_id), str(sitemap_id), sitemap_url
                )
            )
            assert sitemap_task.url == sitemap_url
            assert sitemap_task.website_id == website_id
            assert sitemap_task.sitemap_id == sitemap_id
            assert sitemap_task.is_active is True
