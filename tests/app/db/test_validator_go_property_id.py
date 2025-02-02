import pytest

from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT
from app.db.validators import validate_property_id_required


def test_validate_property_id_required() -> None:
    assert validate_property_id_required(cls=None, value="valid_id") == "valid_id"
    assert validate_property_id_required(cls=None, value="0") == "0"
    assert (
        validate_property_id_required(cls=None, value="a" * DB_STR_16BIT_MAXLEN_INPUT)
        == "a" * DB_STR_16BIT_MAXLEN_INPUT
    )
    with pytest.raises(ValueError):
        assert validate_property_id_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_property_id_required(
            cls=None, value="a" * (DB_STR_16BIT_MAXLEN_INPUT + 1)
        )
