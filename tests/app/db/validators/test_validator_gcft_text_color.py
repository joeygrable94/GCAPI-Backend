import pytest

from app.db.constants import DB_STR_32BIT_MAXLEN_INPUT
from app.db.validators import validate_text_color_optional


def test_validate_text_color_optional() -> None:
    assert validate_text_color_optional(cls=None, value=None) is None
    assert validate_text_color_optional(cls=None, value="red") == "red"
    assert validate_text_color_optional(cls=None, value="green") == "green"
    assert validate_text_color_optional(cls=None, value="blue") == "blue"
    assert validate_text_color_optional(cls=None, value="black") == "black"
    assert validate_text_color_optional(cls=None, value="white") == "white"
    assert validate_text_color_optional(cls=None, value="yellow") == "yellow"
    assert validate_text_color_optional(cls=None, value="purple") == "purple"
    assert validate_text_color_optional(cls=None, value="orange") == "orange"
    assert validate_text_color_optional(cls=None, value="pink") == "pink"
    assert validate_text_color_optional(cls=None, value="brown") == "brown"
    assert validate_text_color_optional(cls=None, value="gray") == "gray"
    assert validate_text_color_optional(cls=None, value="grey") == "grey"
    assert validate_text_color_optional(cls=None, value="") == ""
    with pytest.raises(ValueError):
        validate_text_color_optional(
            cls=None, value="a" * (DB_STR_32BIT_MAXLEN_INPUT + 1)
        )
