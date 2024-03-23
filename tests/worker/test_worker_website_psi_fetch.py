from unittest.mock import Mock, patch

import pytest
from tests.utils.website_pagespeedinsights import generate_psi_base

from app.core.utilities.uuids import get_uuid
from app.schemas import PageSpeedInsightsDevice
from app.schemas.website_pagespeedinsights import PSIDevice
from app.tasks import task_website_page_pagespeedinsights_fetch


@pytest.mark.anyio
async def test_celery_task_website_page_pagespeedinsights_fetch() -> None:
    website_id = get_uuid()
    page_id = get_uuid()
    psi_url = "https://getcommunity.com/"
    mock_psi_insights_base = generate_psi_base()
    mock_fetch = Mock(return_value=mock_psi_insights_base)

    with patch("app.tasks.website_tasks.fetch_pagespeedinsights", new=mock_fetch):
        result = await task_website_page_pagespeedinsights_fetch(
            website_id=str(website_id),
            page_id=str(page_id),
            fetch_url=str(psi_url),
            device=PSIDevice.desktop,
        )

    assert str(result.website_id) == str(website_id)
    assert str(result.page_id) == str(page_id)
    assert result.insights == mock_psi_insights_base
    mock_fetch.assert_called_once_with(
        fetch_url=psi_url, device=PageSpeedInsightsDevice(device="desktop")
    )
