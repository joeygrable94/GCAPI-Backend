import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_snap_name_optional, validate_snap_name_required


def test_validate_snap_name_required() -> None:
    assert (
        validate_snap_name_required(cls=None, value="Valid Snap Name")
        == "Valid Snap Name"
    )
    with pytest.raises(ValueError):
        validate_snap_name_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_snap_name_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_snap_name_required(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )


def test_validate_snap_name_optional() -> None:
    assert validate_snap_name_optional(cls=None, value=None) is None
    assert (
        validate_snap_name_optional(cls=None, value="Valid Snap Name")
        == "Valid Snap Name"
    )
    with pytest.raises(ValueError):
        assert validate_snap_name_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_snap_name_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
