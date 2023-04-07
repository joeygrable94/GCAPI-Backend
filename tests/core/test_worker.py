from typing import Any

import pytest
from tests.utils.utils import random_lower_string

from app.core.utilities.uuids import get_uuid
from app.worker import task_website_sitemap_fetch_url, task_speak


@pytest.mark.celery
def test_celery_task_speak(celery_worker: Any) -> None:
    random_word = random_lower_string()
    result = task_speak(word=random_word)
    assert result == f"I say, {random_word}!"

'''
@pytest.mark.celery
def test_celery_task_website_sitemap_fetch_url(celery_worker: Any) -> None:
    website_id = get_uuid()
    sitemap_url = "https://getcommunity.com/"
    result = task_website_sitemap_fetch_url(website_id, sitemap_url)
    assert result is None
'''
