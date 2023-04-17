from typing import Any
from unittest.mock import Mock, patch

import pytest
from tests.utils.website_pagespeedinsights import generate_psi_base

from app.core.utilities.uuids import get_uuid
from app.schemas import PageSpeedInsightsDevice, WebsitePageSpeedInsightsProcessing
from app.worker import task_website_page_pagespeedinsights_fetch


@pytest.mark.celery
@pytest.mark.asyncio
async def test_celery_task_website_page_pagespeedinsights_fetch(celery_worker: Any) -> None:
    website_id = get_uuid()
    page_id = get_uuid()
    psi_url = "https://getcommunity.com/"
    mock_psi_insights_base = generate_psi_base()
    mock_fetch = Mock(return_value=mock_psi_insights_base)

    with patch("app.worker.fetch_pagespeedinsights", new=mock_fetch):
        result: WebsitePageSpeedInsightsProcessing = task_website_page_pagespeedinsights_fetch(
            website_id, page_id, psi_url, "desktop"
        )

    assert result["website_id"] == website_id
    assert result["page_id"] == page_id
    assert result["insights"] == mock_psi_insights_base
    mock_fetch.assert_called_once_with(
        fetch_url=psi_url, device=PageSpeedInsightsDevice(device="desktop")
    )
