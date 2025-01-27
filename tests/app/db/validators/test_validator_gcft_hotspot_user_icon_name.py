import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_hotspot_user_icon_name_optional


def test_validate_hotspot_user_icon_name_optional() -> None:
    assert validate_hotspot_user_icon_name_optional(cls=None, value=None) is None
    assert (
        validate_hotspot_user_icon_name_optional(
            cls=None, value="Valid Hotspot User Icon Name"
        )
        == "Valid Hotspot User Icon Name"
    )
    with pytest.raises(ValueError):
        validate_hotspot_user_icon_name_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
