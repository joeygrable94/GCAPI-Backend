import pytest

from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT
from app.db.validators import validate_group_slug_required


def test_validate_group_slug_required() -> None:
    assert validate_group_slug_required(cls=None, value="valid_slug") == "valid_slug"
    assert validate_group_slug_required(cls=None, value="a" * 12) == "a" * 12
    with pytest.raises(ValueError):
        assert validate_group_slug_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_group_slug_required(
            cls=None, value="a" * (DB_STR_16BIT_MAXLEN_INPUT + 1)
        )
