import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_country_optional


def test_validate_country_optional() -> None:
    assert validate_country_optional(cls=None, value=None) is None
    assert validate_country_optional(cls=None, value="") == ""
    assert validate_country_optional(cls=None, value="United States") == "United States"
    assert validate_country_optional(cls=None, value="Canada") == "Canada"
    with pytest.raises(ValueError):
        validate_country_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
