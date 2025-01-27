import pytest

from app.db.validators import validate_keys_optional, validate_keys_required
from tests.constants.limits import BLOB_MAX_STR, LONGTEXT_MAX_STR


def test_validate_keys_required() -> None:
    assert validate_keys_required(cls=None, value="Valid Keys") == "Valid Keys"
    with pytest.raises(ValueError):
        assert validate_keys_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_keys_required(cls=None, value=LONGTEXT_MAX_STR + "a")


def test_validate_keys_optional() -> None:
    assert validate_keys_optional(cls=None, value=None) is None
    assert validate_keys_optional(cls=None, value="valid keys") == "valid keys"
    assert validate_keys_optional(cls=None, value=BLOB_MAX_STR) == BLOB_MAX_STR
    with pytest.raises(ValueError):
        assert validate_keys_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_keys_optional(cls=None, value=LONGTEXT_MAX_STR + "a")
