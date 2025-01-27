import pytest

from app.db.constants import DB_INT_ALTITUDE_MAX
from app.db.validators import validate_altitude_optional, validate_altitude_required


def test_validate_altitude_required() -> None:
    assert validate_altitude_required(cls=None, value=0) == 0
    assert validate_altitude_required(cls=None, value=500) == 500
    assert (
        validate_altitude_required(cls=None, value=DB_INT_ALTITUDE_MAX)
        == DB_INT_ALTITUDE_MAX
    )
    with pytest.raises(ValueError):
        assert validate_altitude_required(cls=None, value=-1)
    with pytest.raises(ValueError):
        validate_altitude_required(cls=None, value=-1)
    with pytest.raises(ValueError):
        validate_altitude_required(cls=None, value=DB_INT_ALTITUDE_MAX + 1)


def test_validate_altitude_optional() -> None:
    assert validate_altitude_optional(cls=None, value=None) is None
    assert validate_altitude_optional(cls=None, value=0) == 0
    assert validate_altitude_optional(cls=None, value=500) == 500
    assert (
        validate_altitude_optional(cls=None, value=DB_INT_ALTITUDE_MAX)
        == DB_INT_ALTITUDE_MAX
    )
    with pytest.raises(ValueError):
        assert validate_altitude_optional(cls=None, value=-1)
    with pytest.raises(ValueError):
        validate_altitude_optional(cls=None, value=-1)
    with pytest.raises(ValueError):
        validate_altitude_optional(cls=None, value=DB_INT_ALTITUDE_MAX + 1)
