from typing import Any

import pytest

from app.entities.website_pagespeedinsight.schemas import PageSpeedInsightsDevice


def test_psi_device_validator() -> Any:
    with pytest.raises(ValueError):
        PageSpeedInsightsDevice(device="")
    with pytest.raises(ValueError):
        PageSpeedInsightsDevice(device="aPPle")
