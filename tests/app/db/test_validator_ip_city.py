import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_ip_city_optional


def test_validate_ip_city_optional() -> None:
    assert validate_ip_city_optional(cls=None, value=None) is None
    assert (
        validate_ip_city_optional(cls=None, value="Valid Location") == "Valid Location"
    )
    with pytest.raises(ValueError):
        validate_ip_city_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
