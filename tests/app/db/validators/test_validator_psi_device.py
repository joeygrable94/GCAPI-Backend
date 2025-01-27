import pytest

from app.db.validators import validate_device_required, validate_strategy_required


def test_validate_device_required() -> None:
    assert validate_device_required(cls=None, value="mobile") == "mobile"
    assert validate_device_required(cls=None, value="desktop") == "desktop"
    assert validate_device_required(cls=None, value="Mobile") == "mobile"
    with pytest.raises(ValueError):
        validate_device_required(cls=None, value="laptop")
    with pytest.raises(ValueError):
        validate_device_required(cls=None, value=None)  # type: ignore


def test_validate_strategy_required() -> None:
    assert validate_strategy_required(cls=None, value="mobile") == "mobile"
    assert validate_strategy_required(cls=None, value="desktop") == "desktop"
    with pytest.raises(ValueError):
        validate_strategy_required(cls=None, value="web")
    with pytest.raises(ValueError):
        validate_strategy_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_strategy_required(cls=None, value="")
