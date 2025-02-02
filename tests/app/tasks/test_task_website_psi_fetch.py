from unittest.mock import Mock, patch

import pytest

from app.entities.website_pagespeedinsight.schemas import (
    PageSpeedInsightsDevice,
    PSIDevice,
)
from app.tasks.background import bg_task_website_page_pagespeedinsights_fetch
from app.utilities.uuids import get_uuid
from tests.utils.website_pagespeedinsights import generate_psi_base


@pytest.mark.anyio
async def test_worker_task_website_page_pagespeedinsights_fetch() -> None:
    website_id = get_uuid()
    page_id = get_uuid()
    psi_url = "https://getcommunity.com/"
    mock_psi_insights_base = generate_psi_base()
    mock_fetch = Mock(return_value=mock_psi_insights_base)
    with patch("app.tasks.background.fetch_pagespeedinsights", new=mock_fetch):
        await bg_task_website_page_pagespeedinsights_fetch(
            website_id=str(website_id),
            page_id=str(page_id),
            fetch_url=str(psi_url),
            device=PSIDevice.desktop,
        )
    mock_fetch.assert_called_once_with(
        fetch_url=psi_url, device=PageSpeedInsightsDevice(device=PSIDevice.desktop)
    )
