import pytest

from app.db.constants import DB_INT_INTEGER_MAXLEN_STORED
from app.db.validators import (
    validate_impressions_optional,
    validate_impressions_required,
)


def test_validate_impressions_required() -> None:
    assert validate_impressions_required(cls=None, value=0) == 0
    assert validate_impressions_required(cls=None, value=1) == 1
    assert (
        validate_impressions_required(cls=None, value=DB_INT_INTEGER_MAXLEN_STORED)
        == DB_INT_INTEGER_MAXLEN_STORED
    )
    with pytest.raises(ValueError):
        validate_impressions_required(cls=None, value=-1)
    with pytest.raises(ValueError):
        validate_impressions_required(cls=None, value=DB_INT_INTEGER_MAXLEN_STORED + 1)


def test_validate_impressions_optional() -> None:
    assert validate_impressions_optional(cls=None, value=0) == 0
    assert validate_impressions_optional(cls=None, value=None) is None
    assert (
        validate_impressions_optional(cls=None, value=DB_INT_INTEGER_MAXLEN_STORED)
        == DB_INT_INTEGER_MAXLEN_STORED
    )
    with pytest.raises(ValueError):
        validate_impressions_optional(cls=None, value=-1)
    with pytest.raises(ValueError):
        validate_impressions_optional(cls=None, value=DB_INT_INTEGER_MAXLEN_STORED + 1)
