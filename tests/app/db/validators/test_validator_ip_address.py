import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_ip_address_optional, validate_ip_address_required


def test_validate_ip_address_required() -> None:
    assert validate_ip_address_required(cls=None, value="192.168.0.1") == "192.168.0.1"
    assert validate_ip_address_required(cls=None, value="::1") == "::1"
    assert (
        validate_ip_address_required(
            cls=None, value="2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        )
        == "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    )
    with pytest.raises(ValueError):
        validate_ip_address_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_ip_address_required(cls=None, value=None)  # type: ignore


def test_validate_ip_address_optional() -> None:
    assert validate_ip_address_optional(cls=None, value=None) is None
    assert validate_ip_address_optional(cls=None, value="192.168.0.1") == "192.168.0.1"
    assert (
        validate_ip_address_optional(
            cls=None, value="2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        )
        == "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    )
    with pytest.raises(ValueError):
        validate_ip_address_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_ip_address_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
