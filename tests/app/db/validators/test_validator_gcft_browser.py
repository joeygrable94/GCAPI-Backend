import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_browser_optional


def test_validate_browser_optional() -> None:
    assert validate_browser_optional(cls=None, value=None) is None
    assert validate_browser_optional(cls=None, value="Valid Browser") == "Valid Browser"
    with pytest.raises(ValueError):
        validate_browser_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
