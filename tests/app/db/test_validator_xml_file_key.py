import pytest

from app.db.constants import DB_STR_32BIT_MAXLEN_INPUT
from app.db.validators import validate_xml_file_key_required


def test_validate_xml_file_key_required() -> None:
    max_boundary = "a" * DB_STR_32BIT_MAXLEN_INPUT
    assert validate_xml_file_key_required(cls=None, value="valid-key") == "valid-key"
    assert validate_xml_file_key_required(cls=None, value=max_boundary) == max_boundary
    with pytest.raises(ValueError):
        assert validate_xml_file_key_required(cls=None, value="")
    with pytest.raises(ValueError):
        assert validate_xml_file_key_required(cls=None, value="as")
    with pytest.raises(ValueError):
        validate_xml_file_key_required(cls=None, value="a" + max_boundary)
