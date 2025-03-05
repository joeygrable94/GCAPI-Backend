import pytest

from app.entities.tracking_link.schemas import TrackingLinkBaseParams
from app.entities.tracking_link.utilities import parse_url_utm_params


@pytest.mark.parametrize(
    "url,expected",
    [
        (
            "https://example.com/some/path?utm_source=google&utm_medium=email&utm_campaign=test_campaign",
            TrackingLinkBaseParams(
                scheme="https",
                domain="example.com",
                destination="https://example.com/some/path",
                url_path="/some/path",
                utm_source="google",
                utm_medium="email",
                utm_campaign="test_campaign",
            ),
        ),
        (
            "https://example.com/some/path?utm_source=google&utm_medium=email&utm_campaign=test_campaign&utm_content=asdf_1234",
            TrackingLinkBaseParams(
                scheme="https",
                domain="example.com",
                destination="https://example.com/some/path",
                url_path="/some/path",
                utm_source="google",
                utm_medium="email",
                utm_campaign="test_campaign",
                utm_content="asdf_1234",
            ),
        ),
        (
            "http://example.org/path?utm_source=facebook&utm_term=keywords",
            TrackingLinkBaseParams(
                scheme="http",
                domain="example.org",
                destination="http://example.org/path",
                url_path="/path",
                utm_source="facebook",
                utm_term="keywords",
            ),
        ),
        (
            "https://example.net/path",
            TrackingLinkBaseParams(
                scheme="https",
                domain="example.net",
                destination="https://example.net/path",
                url_path="/path",
            ),
        ),
    ],
    ids=[
        "valid url with all utm params",
        "valid url with all utm params and extra content param",
        "valid url with source and term utm params",
        "valid url without utm params",
    ],
)
def test_parse_url_utm_params_valid(url, expected):
    result = parse_url_utm_params(url)

    assert result == expected


def test_parse_url_utm_params_invalid_url():
    invalid_url = "not-a-valid-url"

    with pytest.raises(Exception):
        parse_url_utm_params(invalid_url)


def test_parse_url_utm_params_missing_utm_params():
    url_without_utm = "https://example.com/no-utm"

    result = parse_url_utm_params(url_without_utm)

    assert result.scheme == "https"
    assert result.domain == "example.com"
    assert result.destination == "https://example.com/no-utm"
    assert result.url_path == "/no-utm"
    assert result.utm_source is None
    assert result.utm_medium is None
    assert result.utm_campaign is None
    assert result.utm_content is None
    assert result.utm_term is None


def test_parse_url_utm_params_unexpected_query_params():
    url_with_extra_params = "https://example.com/path?utm_source=google&utm_campaign=campaign&extra_param=test"

    result = parse_url_utm_params(url_with_extra_params)

    assert result.utm_source == "google"
    assert result.utm_campaign == "campaign"
    assert hasattr(result, "utm_medium")
