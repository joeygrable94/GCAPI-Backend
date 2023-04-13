import json
import os
from typing import Any, Dict
from unittest.mock import MagicMock, patch

from pydantic import AnyHttpUrl

from app.api.utils import fetch_pagespeedinsights
from app.schemas import PageSpeedInsightsDevice


def test_fetch_pagespeedinsights(mock_fetch_psi: Dict[str, Any]) -> None:
    fetch_url: AnyHttpUrl = "https://getcommunity.com"  # type: ignore
    strategy: PageSpeedInsightsDevice = PageSpeedInsightsDevice(device="mobile")
    api_key: str | None = os.environ.get("GOOGLE_CLOUD_API_KEY", None)
    if api_key is None:
        raise Exception("Google Cloud API Key not found in environment variables")

    with patch("app.api.utils.request.urlopen") as mock_urlopen:
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
