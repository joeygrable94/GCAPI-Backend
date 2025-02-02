import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_address_optional, validate_address_required
from tests.constants.limits import LONGTEXT_MAX_STR


def test_validate_address_required() -> None:
    assert validate_address_required(cls=None, value="Valid Address") == "Valid Address"
    with pytest.raises(ValueError):
        assert validate_address_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_address_required(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
    with pytest.raises(ValueError):
        validate_address_required(cls=None, value=None)  # type: ignore


def test_validate_address_optional() -> None:
    assert validate_address_optional(cls=None, value=None) is None
    assert validate_address_optional(cls=None, value="Valid Address") == "Valid Address"
    with pytest.raises(ValueError):
        validate_address_optional(cls=None, value=LONGTEXT_MAX_STR + "a")
