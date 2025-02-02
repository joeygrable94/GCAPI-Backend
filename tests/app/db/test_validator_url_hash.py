import pytest

from app.db.constants import DB_STR_URLPATH_MAXLEN_INPUT
from app.db.validators import validate_url_hash_optional, validate_url_hash_required


def test_validate_url_hash_required() -> None:
    assert validate_url_hash_required(cls=None, value="hash") == "hash"
    with pytest.raises(ValueError):
        validate_url_hash_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_url_hash_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_url_hash_required(
            cls=None,
            value="hash" + "a" * (DB_STR_URLPATH_MAXLEN_INPUT + 1),
        )


def test_validate_url_hash_optional() -> None:
    assert validate_url_hash_optional(cls=None, value=None) is None
    assert validate_url_hash_optional(cls=None, value="hash") == "hash"
    with pytest.raises(ValueError):
        validate_url_hash_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_url_hash_optional(
            cls=None,
            value="hash" + "a" * (DB_STR_URLPATH_MAXLEN_INPUT + 1),
        )
