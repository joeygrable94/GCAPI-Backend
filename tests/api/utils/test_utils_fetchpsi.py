import os
import json
from unittest.mock import MagicMock, patch

import pytest

from app.schemas import PageSpeedInsightsDevice
from app.worker import fetch_pagespeedinsights


@pytest.mark.asyncio
async def test_fetch_pagespeedinsights():
    fetch_url = "https://getcommunity.com"
    strategy = PageSpeedInsightsDevice(device="mobile")
    api_key: str | None = os.environ.get("GOOGLE_CLOUD_API_KEY", None)
    if api_key is None:
        raise Exception("Google Cloud API Key not found in environment variables")

    mocked_response = {}
    here = os.path.dirname(os.path.abspath(__file__))
    with open(f'{here}/fetchpsi.json') as f:
        mocked_response = json.load(f)

    with patch("app.api.utils.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mocked_response).encode("utf-8")
        mock_urlopen.return_value = mock_response

        await fetch_pagespeedinsights(fetch_url, strategy)

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
