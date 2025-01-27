import pytest

from app.db.validators import validate_bg_color_optional


def test_validate_bg_color_optional() -> None:
    assert validate_bg_color_optional(cls=None, value=None) is None
    assert validate_bg_color_optional(cls=None, value="") == ""
    assert validate_bg_color_optional(cls=None, value="red") == "red"
    assert validate_bg_color_optional(cls=None, value="green") == "green"
    assert validate_bg_color_optional(cls=None, value="blue") == "blue"
    assert validate_bg_color_optional(cls=None, value="yellow") == "yellow"
    assert validate_bg_color_optional(cls=None, value="purple") == "purple"
    assert validate_bg_color_optional(cls=None, value="orange") == "orange"
    assert validate_bg_color_optional(cls=None, value="black") == "black"
    assert validate_bg_color_optional(cls=None, value="white") == "white"
    assert validate_bg_color_optional(cls=None, value="gray") == "gray"
    assert validate_bg_color_optional(cls=None, value="grey") == "grey"
    assert validate_bg_color_optional(cls=None, value="pink") == "pink"
    assert validate_bg_color_optional(cls=None, value="brown") == "brown"
    assert validate_bg_color_optional(cls=None, value="cyan") == "cyan"
    assert validate_bg_color_optional(cls=None, value="magenta") == "magenta"
    assert validate_bg_color_optional(cls=None, value="teal") == "teal"
    assert validate_bg_color_optional(cls=None, value="navy") == "navy"
    assert validate_bg_color_optional(cls=None, value="maroon") == "maroon"
    assert validate_bg_color_optional(cls=None, value="olive") == "olive"
    assert validate_bg_color_optional(cls=None, value="silver") == "silver"
    assert validate_bg_color_optional(cls=None, value="lime") == "lime"
    assert validate_bg_color_optional(cls=None, value="aqua") == "aqua"
    assert validate_bg_color_optional(cls=None, value="fuchsia") == "fuchsia"
    with pytest.raises(ValueError):
        validate_bg_color_optional(cls=None, value="red" * 11)
