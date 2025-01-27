import pytest

from app.db.validators import validate_rawtext_optional, validate_rawtext_required
from tests.constants.limits import LONGTEXT_MAX_STR


def test_validate_rawtext_required() -> None:
    assert validate_rawtext_required(cls=None, value="Valid Rawtext") == "Valid Rawtext"
    with pytest.raises(ValueError):
        validate_rawtext_required(cls=None, value=LONGTEXT_MAX_STR + "a")
    with pytest.raises(ValueError):
        validate_rawtext_required(cls=None, value=None)  # type: ignore


def test_validate_rawtext_optional() -> None:
    assert validate_rawtext_optional(cls=None, value=None) is None
    assert validate_rawtext_optional(cls=None, value="Valid Rawtext") == "Valid Rawtext"
    with pytest.raises(ValueError):
        validate_rawtext_optional(cls=None, value=LONGTEXT_MAX_STR + "a")
