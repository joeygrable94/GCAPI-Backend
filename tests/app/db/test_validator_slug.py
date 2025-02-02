import pytest

from app.db.constants import DB_STR_64BIT_MAXLEN_INPUT
from app.db.validators import validate_slug_optional, validate_slug_required


def test_validate_slug_required() -> None:
    assert validate_slug_required(cls=None, value="valid-slug") == "valid-slug"
    with pytest.raises(ValueError):
        validate_slug_required(cls=None, value="sl")
    with pytest.raises(ValueError):
        validate_slug_required(cls=None, value="a" * (DB_STR_64BIT_MAXLEN_INPUT + 1))
    with pytest.raises(ValueError):
        validate_slug_required(cls=None, value=None)  # type: ignore


def test_validate_slug_optional() -> None:
    assert validate_slug_optional(cls=None, value="valid-slug") == "valid-slug"
    assert validate_slug_optional(cls=None, value=None) is None
    with pytest.raises(ValueError):
        validate_slug_optional(cls=None, value="sl")
    with pytest.raises(ValueError):
        validate_slug_optional(cls=None, value="a" * (DB_STR_64BIT_MAXLEN_INPUT + 1))
