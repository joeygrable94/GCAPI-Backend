import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_title_optional, validate_title_required


def test_validate_title_required() -> None:
    assert validate_title_required(cls=None, value="Valid Title") == "Valid Title"
    with pytest.raises(ValueError):
        validate_title_required(cls=None, value="a")
    with pytest.raises(ValueError):
        validate_title_required(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
    with pytest.raises(ValueError):
        validate_title_required(cls=None, value=None)  # type: ignore


def test_validate_title_optional() -> None:
    assert validate_title_optional(cls=None, value=None) is None
    assert validate_title_optional(cls=None, value="Valid Title") == "Valid Title"
    with pytest.raises(ValueError):
        validate_title_optional(cls=None, value="a")
    with pytest.raises(ValueError):
        validate_title_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
