import pytest

from app.db.validators import validate_platform_optional
from tests.constants.limits import LONGTEXT_MAX_STR


def test_validate_platform_optional() -> None:
    assert validate_platform_optional(cls=None, value=None) is None
    assert (
        validate_platform_optional(cls=None, value="Valid Platform") == "Valid Platform"
    )
    assert validate_platform_optional(cls=None, value="") == ""
    with pytest.raises(ValueError):
        validate_platform_optional(cls=None, value=LONGTEXT_MAX_STR + "a")
