import pytest

from app.db.constants import DB_STR_DESC_MAXLEN_INPUT, DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_description_optional, validate_domain_required


def test_validate_description_optional() -> None:
    assert validate_description_optional(cls=None, value=None) is None
    assert (
        validate_description_optional(cls=None, value="Valid Description")
        == "Valid Description"
    )
    with pytest.raises(ValueError):
        validate_description_optional(
            cls=None, value="a" * (DB_STR_DESC_MAXLEN_INPUT + 1)
        )


def test_validate_domain_required() -> None:
    assert validate_domain_required(cls=None, value="example.com") == "example.com"
    assert (
        validate_domain_required(cls=None, value="subdomain.example.com")
        == "subdomain.example.com"
    )
    with pytest.raises(ValueError):
        validate_domain_required(cls=None, value="example.com/path")
    with pytest.raises(ValueError):
        validate_domain_required(cls=None, value="example")
    with pytest.raises(ValueError):
        validate_domain_required(cls=None, value="example.")
    with pytest.raises(ValueError):
        validate_domain_required(cls=None, value=".example.com")
    with pytest.raises(ValueError):
        validate_domain_required(
            cls=None, value="example.com" + "a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
    with pytest.raises(ValueError):
        validate_domain_required(
            cls=None,
            value="example.com/path" + "a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1),
        )
    with pytest.raises(ValueError):
        validate_domain_required(cls=None, value=None)  # type: ignore
