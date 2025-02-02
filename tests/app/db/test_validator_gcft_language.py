import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_language_optional


def test_validate_language_optional() -> None:
    assert validate_language_optional(cls=None, value=None) is None
    assert validate_language_optional(cls=None, value="") == ""
    assert validate_language_optional(cls=None, value="English") == "English"
    assert validate_language_optional(cls=None, value="French") == "French"
    assert validate_language_optional(cls=None, value="Spanish") == "Spanish"
    with pytest.raises(ValueError):
        validate_language_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
