import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_snap_file_name_optional


def test_validate_snap_file_name_optional() -> None:
    assert validate_snap_file_name_optional(cls=None, value=None) is None
    assert (
        validate_snap_file_name_optional(cls=None, value="valid_file_name.jpg")
        == "valid_file_name.jpg"
    )
    with pytest.raises(ValueError):
        validate_snap_file_name_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
