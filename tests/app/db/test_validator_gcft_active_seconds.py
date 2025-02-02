import pytest

from app.db.validators import validate_active_seconds_required


def test_validate_active_seconds_required() -> None:
    assert validate_active_seconds_required(cls=None, value=0) == 0
    assert validate_active_seconds_required(cls=None, value=86400) == 86400
    assert validate_active_seconds_required(cls=None, value=60) == 60
    with pytest.raises(ValueError):
        validate_active_seconds_required(cls=None, value=-1)
    with pytest.raises(ValueError):
        validate_active_seconds_required(cls=None, value=86401)
