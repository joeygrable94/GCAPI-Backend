import pytest

from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT
from app.db.validators import validate_snap_slug_required


def test_validate_snap_slug_required() -> None:
    assert validate_snap_slug_required(cls=None, value="validslug") == "validslug"
    assert validate_snap_slug_required(cls=None, value="123456789012") == "123456789012"
    with pytest.raises(ValueError):
        assert validate_snap_slug_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_snap_slug_required(
            cls=None, value="a" * (DB_STR_16BIT_MAXLEN_INPUT + 1)
        )
