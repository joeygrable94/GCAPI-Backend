import pytest

from app.db.constants import DB_STR_64BIT_MAXLEN_INPUT
from app.db.validators import validate_change_type_required


def test_validate_change_type_required() -> None:
    assert validate_change_type_required(cls=None, value="valid-slug") == "valid-slug"
    with pytest.raises(ValueError):
        validate_change_type_required(cls=None, value="sl")
    with pytest.raises(ValueError):
        validate_change_type_required(
            cls=None, value="a" * (DB_STR_64BIT_MAXLEN_INPUT + 1)
        )
    with pytest.raises(ValueError):
        validate_change_type_required(cls=None, value=None)  # type: ignore
