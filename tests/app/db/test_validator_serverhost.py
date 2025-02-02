import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_serverhost_optional, validate_serverhost_required


def test_validate_serverhost_required() -> None:
    assert validate_serverhost_required(cls=None, value="example.com") == "example.com"
    assert (
        validate_serverhost_required(cls=None, value="subdomain.example.com")
        == "subdomain.example.com"
    )
    with pytest.raises(ValueError):
        assert validate_serverhost_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_serverhost_required(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )


def test_validate_serverhost_optional() -> None:
    assert validate_serverhost_optional(cls=None, value=None) is None
    assert validate_serverhost_optional(cls=None, value="example.com") == "example.com"
    assert (
        validate_serverhost_optional(cls=None, value="subdomain.example.com")
        == "subdomain.example.com"
    )
    with pytest.raises(ValueError):
        validate_serverhost_optional(cls=None, value="a")
    with pytest.raises(ValueError):
        validate_serverhost_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
