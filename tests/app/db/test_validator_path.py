import pytest

from app.db.constants import DB_STR_URLPATH_MAXLEN_INPUT
from app.db.validators import validate_url_path_optional, validate_url_path_required


def test_validate_url_path_required() -> None:
    assert validate_url_path_required(cls=None, value="/asdf/asdf") == "/asdf/asdf"
    with pytest.raises(ValueError):
        validate_url_path_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_url_path_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_url_path_required(
            cls=None,
            value="path/" + "a" * (DB_STR_URLPATH_MAXLEN_INPUT + 1),
        )


def test_validate_url_path_optional() -> None:
    assert validate_url_path_optional(cls=None, value=None) is None
    assert validate_url_path_optional(cls=None, value="/") == "/"
    assert validate_url_path_optional(cls=None, value="/path") == "/path"
    assert (
        validate_url_path_optional(cls=None, value="/path?query=string")
        == "/path?query=string"
    )
    assert validate_url_path_optional(cls=None, value="/") == "/"
    with pytest.raises(ValueError):
        validate_url_path_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_url_path_optional(
            cls=None,
            value="http://example.com/path" + "a" * (DB_STR_URLPATH_MAXLEN_INPUT + 1),
        )
