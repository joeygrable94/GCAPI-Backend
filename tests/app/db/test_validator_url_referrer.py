import pytest

from app.db.constants import DB_STR_URLPATH_MAXLEN_INPUT
from app.db.validators import validate_referrer_required


def test_validate_referrer_required() -> None:
    assert (
        validate_referrer_required(cls=None, value="https://example.com")
        == "https://example.com"
    )
    assert (
        validate_referrer_required(cls=None, value="https://example.com/path")
        == "https://example.com/path"
    )
    assert validate_referrer_required(cls=None, value="/") == "/"
    with pytest.raises(ValueError):
        validate_referrer_required(
            cls=None,
            value="http://example.com/path" + "a" * (DB_STR_URLPATH_MAXLEN_INPUT + 1),
        )
    with pytest.raises(ValueError):
        validate_referrer_required(cls=None, value=None)  # type: ignore
