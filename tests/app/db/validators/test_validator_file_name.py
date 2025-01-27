import pytest

from app.db.constants import (
    DB_STR_BUCKET_OBJECT_NAME_MAXLEN_INPUT,
    DB_STR_BUCKET_OBJECT_NAME_MINLEN_INPUT,
)
from app.db.validators import validate_file_name_optional, validate_file_name_required


def test_validate_file_name_required() -> None:
    assert validate_file_name_required(cls=None, value="ValidName") == "ValidName"
    with pytest.raises(ValueError):
        assert validate_file_name_required(
            cls=None, value="a" * (DB_STR_BUCKET_OBJECT_NAME_MINLEN_INPUT - 1)
        )
    with pytest.raises(ValueError):
        validate_file_name_required(
            cls=None, value="a" * (DB_STR_BUCKET_OBJECT_NAME_MAXLEN_INPUT + 1)
        )


def test_validate_file_name_optional() -> None:
    assert validate_file_name_optional(cls=None, value=None) is None
    assert validate_file_name_optional(cls=None, value="ValidName") == "ValidName"
    with pytest.raises(ValueError):
        validate_file_name_optional(
            cls=None, value="a" * (DB_STR_BUCKET_OBJECT_NAME_MINLEN_INPUT - 1)
        )
    with pytest.raises(ValueError):
        validate_file_name_optional(
            cls=None, value="a" * (DB_STR_BUCKET_OBJECT_NAME_MAXLEN_INPUT + 1)
        )
