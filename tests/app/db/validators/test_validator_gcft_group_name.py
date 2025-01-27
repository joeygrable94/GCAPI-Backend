import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_group_name_optional, validate_group_name_required


def test_validate_group_name_required() -> None:
    assert (
        validate_group_name_required(cls=None, value="Valid Group Name")
        == "Valid Group Name"
    )
    with pytest.raises(ValueError):
        validate_group_name_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_group_name_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_group_name_required(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )


def test_validate_group_name_optional() -> None:
    assert validate_group_name_optional(cls=None, value=None) is None
    assert (
        validate_group_name_optional(cls=None, value="Valid Group Name")
        == "Valid Group Name"
    )
    with pytest.raises(ValueError):
        validate_group_name_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
