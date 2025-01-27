import pytest

from app.db.constants import DB_STR_32BIT_MAXLEN_INPUT
from app.db.validators import validate_icon_color_optional


def test_validate_icon_color_optional() -> None:
    assert validate_icon_color_optional(cls=None, value=None) is None
    assert validate_icon_color_optional(cls=None, value="red") == "red"
    assert validate_icon_color_optional(cls=None, value="green") == "green"
    assert validate_icon_color_optional(cls=None, value="blue") == "blue"
    with pytest.raises(ValueError):
        validate_icon_color_optional(
            cls=None, value="a" * (DB_STR_32BIT_MAXLEN_INPUT + 1)
        )
