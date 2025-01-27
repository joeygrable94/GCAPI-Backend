import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_password_optional, validate_password_required


def test_validate_password_required() -> None:
    assert validate_password_required(cls=None, value="password") == "password"
    with pytest.raises(ValueError):
        assert validate_password_required(cls=None, value="")
    assert (
        validate_password_required(cls=None, value="a" * DB_STR_TINYTEXT_MAXLEN_INPUT)
        == "a" * DB_STR_TINYTEXT_MAXLEN_INPUT
    )
    with pytest.raises(ValueError):
        validate_password_required(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )


def test_validate_password_optional() -> None:
    assert validate_password_optional(cls=None, value=None) is None
    assert validate_password_optional(cls=None, value="12345") == "12345"
    assert (
        validate_password_optional(cls=None, value="a" * DB_STR_TINYTEXT_MAXLEN_INPUT)
        == "a" * DB_STR_TINYTEXT_MAXLEN_INPUT
    )
    with pytest.raises(ValueError):
        validate_password_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_password_optional(cls=None, value="1234")
    with pytest.raises(ValueError):
        validate_password_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
