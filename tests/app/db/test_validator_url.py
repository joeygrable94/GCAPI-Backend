import pytest

from app.db.constants import DB_STR_URLPATH_MAXLEN_INPUT
from app.db.validators import validate_url_optional, validate_url_required


def test_validate_url_required() -> None:
    assert (
        validate_url_required(cls=None, value="https://example.com")
        == "https://example.com"
    )
    with pytest.raises(ValueError):
        validate_url_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_url_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_url_required(
            cls=None,
            value="http://example.com/path" + "a" * (DB_STR_URLPATH_MAXLEN_INPUT + 1),
        )


def test_validate_url_optional() -> None:
    assert validate_url_optional(cls=None, value=None) is None
    assert (
        validate_url_optional(cls=None, value="https://example.com")
        == "https://example.com"
    )
    assert (
        validate_url_optional(cls=None, value="https://example.com/path")
        == "https://example.com/path"
    )
    assert (
        validate_url_optional(cls=None, value="https://example.com/path?query=string")
        == "https://example.com/path?query=string"
    )
    assert validate_url_optional(cls=None, value="/") == "/"
    with pytest.raises(ValueError):
        validate_url_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_url_optional(
            cls=None,
            value="http://example.com/path" + "a" * (DB_STR_URLPATH_MAXLEN_INPUT + 1),
        )
