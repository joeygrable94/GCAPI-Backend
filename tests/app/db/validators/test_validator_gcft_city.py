import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_city_optional


def test_validate_city_optional() -> None:
    assert validate_city_optional(cls=None, value=None) is None
    assert validate_city_optional(cls=None, value="New York") == "New York"
    assert validate_city_optional(cls=None, value="San Francisco") == "San Francisco"
    assert validate_city_optional(cls=None, value="Los Angeles") == "Los Angeles"
    with pytest.raises(ValueError):
        validate_city_optional(cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1))
