import json

import pytest

from app.db.validators import validate_styleguide_optional
from tests.constants.limits import BLOB_MAX_STR


def test_validate_styleguide_optional() -> None:
    valid_json = json.dumps(
        {
            "key1": "value1",
            "key2": "value2",
        }
    )
    invalid_json = json.dumps(
        {
            "key1": "value1",
            "key2": "a" + BLOB_MAX_STR,
        }
    )
    assert validate_styleguide_optional(cls=None, value=None) is None
    assert validate_styleguide_optional(cls=None, value=valid_json) == valid_json
    with pytest.raises(ValueError):
        validate_styleguide_optional(cls=None, value="a" + BLOB_MAX_STR)
        validate_styleguide_optional(cls=None, value=invalid_json)
