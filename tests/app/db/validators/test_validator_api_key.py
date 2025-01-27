import pytest

from app.db.constants import DB_STR_64BIT_MAXLEN_INPUT, DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_api_key_optional, validate_api_key_required


def test_validate_api_key_required() -> None:
    assert validate_api_key_required(cls=None, value="valid_api_key") == "valid_api_key"
    assert (
        validate_api_key_required(cls=None, value="a" * DB_STR_64BIT_MAXLEN_INPUT)
        == "a" * DB_STR_64BIT_MAXLEN_INPUT
    )
    with pytest.raises(ValueError):
        assert validate_api_key_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_api_key_required(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )


def test_validate_api_key_optional() -> None:
    assert validate_api_key_optional(cls=None, value="valid_api_key") == "valid_api_key"
    assert (
        validate_api_key_optional(cls=None, value="a" * DB_STR_64BIT_MAXLEN_INPUT)
        == "a" * DB_STR_64BIT_MAXLEN_INPUT
    )
    assert validate_api_key_optional(cls=None, value=None) is None
    with pytest.raises(ValueError):
        assert validate_api_key_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_api_key_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
