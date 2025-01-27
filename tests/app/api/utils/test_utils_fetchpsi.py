import json
from typing import Any
from unittest.mock import MagicMock, patch

from app.api.utilities import fetch_pagespeedinsights
from app.core.config import settings
from app.schemas import PageSpeedInsightsDevice, PSIDevice


def test_fetch_pagespeedinsights(mock_fetch_psi: dict[str, Any]) -> None:
    fetch_url: str = "https://getcommunity.com"  # type: ignore
    strategy: PageSpeedInsightsDevice = PageSpeedInsightsDevice(device=PSIDevice.mobile)
    api_key: str | None = settings.cloud.googleapi
    if api_key is None:
        raise Exception("Google Cloud API Key not found in environment variables")

    with patch(
        "app.api.utilities.web_pagespeedinsights.request.urlopen"
    ) as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_fetch_psi).encode("utf-8")
        mock_urlopen.return_value = mock_response

        fetch_pagespeedinsights(fetch_url, strategy)

        # assert the expected API request was made
        expected_request = "https://%s/%s/%s?url=%s&key=%s&strategy=%s" % (
            "www.googleapis.com/pagespeedonline",
            "v5",
            "runPagespeed",
            fetch_url,
            api_key,
            strategy.device,
        )
        mock_urlopen.assert_called_with(expected_request)
