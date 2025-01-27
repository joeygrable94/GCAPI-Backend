import pytest

from app.db.constants import DB_STR_32BIT_MAXLEN_INPUT
from app.db.validators import validate_ip_loc_optional


def test_validate_ip_loc_optional() -> None:
    assert validate_ip_loc_optional(cls=None, value=None) is None
    assert validate_ip_loc_optional(cls=None, value="valid value") == "valid value"
    with pytest.raises(ValueError):
        validate_ip_loc_optional(cls=None, value="a" * (DB_STR_32BIT_MAXLEN_INPUT + 1))
