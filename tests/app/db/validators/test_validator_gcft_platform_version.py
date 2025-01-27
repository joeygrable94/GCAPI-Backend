import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_platform_version_optional


def test_validate_platform_version_optional() -> None:
    assert validate_platform_version_optional(cls=None, value=None) is None
    assert validate_platform_version_optional(cls=None, value="") == ""
    assert (
        validate_platform_version_optional(cls=None, value="Valid Platform Version")
        == "Valid Platform Version"
    )
    with pytest.raises(ValueError):
        validate_platform_version_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
