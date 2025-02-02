import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_linked_snap_name_optional


def test_validate_linked_snap_name_optional() -> None:
    assert validate_linked_snap_name_optional(cls=None, value=None) is None
    assert (
        validate_linked_snap_name_optional(cls=None, value="Valid Linked Snap Name")
        == "Valid Linked Snap Name"
    )
    with pytest.raises(ValueError):
        validate_linked_snap_name_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
