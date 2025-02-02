import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import (
    validate_hotspot_content_optional,
    validate_hotspot_icon_name_optional,
)
from tests.constants.limits import BLOB_MAX_STR


def test_validate_hotspot_content_optional() -> None:
    assert validate_hotspot_content_optional(cls=None, value=None) is None
    assert (
        validate_hotspot_content_optional(cls=None, value="Valid hotspot content")
        == "Valid hotspot content"
    )
    with pytest.raises(ValueError):
        validate_hotspot_content_optional(cls=None, value="a" + BLOB_MAX_STR)


def test_validate_hotspot_icon_name_optional() -> None:
    assert validate_hotspot_icon_name_optional(cls=None, value=None) is None
    assert (
        validate_hotspot_icon_name_optional(cls=None, value="Valid Icon Name")
        == "Valid Icon Name"
    )
    with pytest.raises(ValueError):
        validate_hotspot_icon_name_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
