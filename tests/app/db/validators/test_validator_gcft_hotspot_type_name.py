import pytest

from app.db.constants import DB_STR_32BIT_MAXLEN_INPUT
from app.db.validators import validate_hotspot_type_name_optional


def test_validate_hotspot_type_name_optional() -> None:
    assert validate_hotspot_type_name_optional(cls=None, value=None) is None
    assert (
        validate_hotspot_type_name_optional(cls=None, value="Valid Name")
        == "Valid Name"
    )
    assert (
        validate_hotspot_type_name_optional(
            cls=None, value="a" * DB_STR_32BIT_MAXLEN_INPUT
        )
        == "a" * DB_STR_32BIT_MAXLEN_INPUT
    )
    with pytest.raises(ValueError):
        validate_hotspot_type_name_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_hotspot_type_name_optional(
            cls=None, value="a" * (DB_STR_32BIT_MAXLEN_INPUT + 1)
        )
