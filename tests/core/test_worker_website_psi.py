'''
from typing import Any

import pytest

from app.core.utilities.uuids import get_uuid
from app.worker import task_fetch_website_page_pagespeedinsights


@pytest.mark.celery
def test_celery_task_fetch_website_page_pagespeedinsights(celery_worker: Any) -> None:
    website_id = get_uuid()
    page_id = get_uuid()
    psi_url = "https://getcommunity.com/"
    result = task_fetch_website_page_pagespeedinsights(
        website_id, page_id, psi_url, "desktop"
    )
    assert result is None
'''
