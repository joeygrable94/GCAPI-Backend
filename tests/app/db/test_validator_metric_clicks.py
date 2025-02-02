import pytest

from app.db.constants import DB_INT_INTEGER_MAXLEN_STORED
from app.db.validators import validate_clicks_optional, validate_clicks_required


def test_validate_clicks_required() -> None:
    assert validate_clicks_required(cls=None, value=0) == 0
    assert (
        validate_clicks_required(cls=None, value=DB_INT_INTEGER_MAXLEN_STORED)
        == DB_INT_INTEGER_MAXLEN_STORED
    )
    with pytest.raises(ValueError):
        validate_clicks_required(cls=None, value=-1)
    with pytest.raises(ValueError):
        validate_clicks_required(cls=None, value=DB_INT_INTEGER_MAXLEN_STORED + 1)


def test_validate_clicks_optional() -> None:
    assert validate_clicks_optional(cls=None, value=0) == 0
    assert validate_clicks_optional(cls=None, value=None) is None
    assert (
        validate_clicks_optional(cls=None, value=DB_INT_INTEGER_MAXLEN_STORED)
        == DB_INT_INTEGER_MAXLEN_STORED
    )
    with pytest.raises(ValueError):
        validate_clicks_optional(cls=None, value=-1)
    with pytest.raises(ValueError):
        validate_clicks_optional(cls=None, value=DB_INT_INTEGER_MAXLEN_STORED + 1)
