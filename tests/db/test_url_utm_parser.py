from typing import Any

from app.db.utilities import parse_url_utm_params
from app.schemas import TrackingLinkBaseParams


def test_psi_device_validator() -> Any:
    test_url = "https://getcommunity.com/the-successful-processing-of-extra-long-links/?utm_campaign=utm_campaign&utm_medium=utm_medium&utm_source=utm_source&utm_content=utm_content&utm_term=utm_term"  # noqa: E501
    url_params: TrackingLinkBaseParams = parse_url_utm_params(test_url)

    assert url_params.scheme == "https"
    assert url_params.domain == "getcommunity.com"
    assert (
        url_params.destination
        == "https://getcommunity.com/the-successful-processing-of-extra-long-links/"
    )
    assert url_params.url_path == "/the-successful-processing-of-extra-long-links/"
    assert url_params.utm_campaign == "utm_campaign"
    assert url_params.utm_medium == "utm_medium"
    assert url_params.utm_source == "utm_source"
    assert url_params.utm_content == "utm_content"
    assert url_params.utm_term == "utm_term"
