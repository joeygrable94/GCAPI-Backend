import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_username_optional, validate_username_required


def test_validate_username_required() -> None:
    assert (
        validate_username_required(cls=None, value="ValidUsername") == "ValidUsername"
    )
    with pytest.raises(ValueError):
        assert validate_username_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_username_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_username_required(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )


def test_validate_username_optional() -> None:
    assert validate_username_optional(cls=None, value=None) is None
    assert (
        validate_username_optional(cls=None, value="valid_username") == "valid_username"
    )
    with pytest.raises(ValueError):
        validate_username_optional(cls=None, value="a")
    with pytest.raises(ValueError):
        validate_username_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
