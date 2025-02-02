import pytest

from app.db.constants import DB_STR_32BIT_MAXLEN_INPUT
from app.db.validators import validate_reporting_id_required


def test_validate_reporting_id_required() -> None:
    assert (
        validate_reporting_id_required(cls=None, value="valid_reporting_id")
        == "valid_reporting_id"
    )
    with pytest.raises(ValueError):
        validate_reporting_id_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_reporting_id_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_reporting_id_required(
            cls=None, value="a" * (DB_STR_32BIT_MAXLEN_INPUT + 1)
        )
