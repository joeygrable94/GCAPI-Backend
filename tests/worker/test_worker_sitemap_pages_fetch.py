import unittest.mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_maps import generate_mock_sitemap

from app.core.utilities.uuids import get_uuid
from app.schemas import WebsiteMapProcessedResult
from app.tasks import task_website_sitemap_fetch_pages


@pytest.mark.anyio
async def test_task_website_sitemap_fetch_pages(
    mock_fetch_sitemap: list,
    db_session: AsyncSession,
) -> None:
    website_id = get_uuid()
    sitemap_id = get_uuid()
    sitemap_url = "https://getcommunity.com/"
    mock_sitemap = generate_mock_sitemap(sitemap_url, mock_fetch_sitemap)

    with unittest.mock.patch(
        "app.tasks.website_tasks.sitemap_tree_for_homepage"
    ) as mock_sitemap_tree:
        mock_sitemap_tree.return_value = mock_sitemap
        sitemap_task: WebsiteMapProcessedResult = (
            await task_website_sitemap_fetch_pages(
                str(website_id), str(sitemap_id), sitemap_url
            )
        )
        assert sitemap_task.url == sitemap_url
        assert str(sitemap_task.website_id) == str(website_id)
        assert str(sitemap_task.sitemap_id) == str(sitemap_id)
        # assert isinstance(sitemap_task.website_map_pages, list)
        # assert len(sitemap_task.website_map_pages) == len(mock_sitemap.pages)

        # Check that the sitemap and sitemap saving functions
        # were called with the correct arguments
        mock_sitemap_tree.assert_called_once_with(sitemap_url)
