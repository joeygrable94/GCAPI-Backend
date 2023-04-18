import unittest.mock
from typing import Any, Dict
from uuid import UUID

import pytest
from tests.utils.website_maps import generate_mock_sitemap

from app.core.utilities.uuids import get_uuid
from app.schemas import WebsiteMapProcessing
from app.worker import task_website_sitemap_fetch_pages


@pytest.mark.celery
def test_task_website_sitemap_fetch_pages(
    celery_worker: Any, mock_fetch_sitemap: Any
) -> None:
    website_id = get_uuid()
    sitemap_url = "https://getcommunity.com/"
    mock_sitemap = generate_mock_sitemap(sitemap_url, mock_fetch_sitemap)

    with unittest.mock.patch(
        "app.worker.sitemap_tree_for_homepage"
    ) as mock_sitemap_tree:
        mock_sitemap_tree.return_value = mock_sitemap

        sitemap_task: WebsiteMapProcessing = task_website_sitemap_fetch_pages(
            website_id, sitemap_url
        )

        assert sitemap_task.url == sitemap_url
        assert sitemap_task.website_id == website_id
        assert isinstance(sitemap_task.task_id, UUID)

        # Check that the sitemap and sitemap saving functions
        # were called with the correct arguments
        mock_sitemap_tree.assert_called_once_with(sitemap_url)
