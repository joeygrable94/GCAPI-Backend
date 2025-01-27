import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_state_optional


def test_validate_state_optional() -> None:
    assert validate_state_optional(cls=None, value=None) is None
    assert validate_state_optional(cls=None, value="") == ""
    assert validate_state_optional(cls=None, value="Valid State") == "Valid State"
    with pytest.raises(ValueError):
        validate_state_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
