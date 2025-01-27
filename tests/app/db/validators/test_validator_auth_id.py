import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_auth_id_required


def test_validate_auth_id_required() -> None:
    assert validate_auth_id_required(cls=None, value="valid_auth_id") == "valid_auth_id"
    assert (
        validate_auth_id_required(cls=None, value="a" * DB_STR_TINYTEXT_MAXLEN_INPUT)
        == "a" * DB_STR_TINYTEXT_MAXLEN_INPUT
    )
    with pytest.raises(ValueError):
        assert validate_auth_id_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_auth_id_required(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
