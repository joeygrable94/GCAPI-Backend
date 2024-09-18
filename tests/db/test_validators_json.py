import pytest

from app.db.constants import DB_STR_BLOB_MAXLEN_STORED
from app.db.validators import validate_style_guide_optional


def test_validate_style_guide_optional() -> None:
    valid_json = {
        "key1": "value1",
        "key2": "value2",
    }
    invalid_json = {
        "key1": "value1",
        "key2": "a" * (DB_STR_BLOB_MAXLEN_STORED + 1),
    }
    assert validate_style_guide_optional(cls=None, value=None) is None
    assert validate_style_guide_optional(cls=None, value=valid_json) == valid_json
    with pytest.raises(ValueError):
        validate_style_guide_optional(
            cls=None, value="a" * (DB_STR_BLOB_MAXLEN_STORED + 1)
        )
        validate_style_guide_optional(cls=None, value=invalid_json)
