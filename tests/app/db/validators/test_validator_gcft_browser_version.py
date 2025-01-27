import pytest

from app.db.validators import validate_browser_version_optional
from tests.constants.limits import LONGTEXT_MAX_STR


def test_validate_browser_version_optional() -> None:
    assert validate_browser_version_optional(cls=None, value=None) is None
    assert (
        validate_browser_version_optional(cls=None, value="Valid Browser Version")
        == "Valid Browser Version"
    )
    with pytest.raises(ValueError):
        validate_browser_version_optional(cls=None, value=LONGTEXT_MAX_STR + "a")
