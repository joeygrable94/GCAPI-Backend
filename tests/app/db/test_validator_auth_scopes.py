import pytest

from app.db.validators import validate_scopes_optional, validate_scopes_required
from app.services.permission import AclPrivilege


def test_validate_scopes_required() -> None:
    assert validate_scopes_required(cls=None, value=["read:test", "write:test"]) == [
        AclPrivilege("read:test"),
        AclPrivilege("write:test"),
    ]
    assert validate_scopes_required(
        cls=None, value=[AclPrivilege("read:test"), AclPrivilege("write:test")]
    ) == [
        AclPrivilege("read:test"),
        AclPrivilege("write:test"),
    ]
    assert validate_scopes_required(cls=None, value=["read:test", "write:test"]) == [
        AclPrivilege("read:test"),
        AclPrivilege("write:test"),
    ]
    with pytest.raises(ValueError):
        validate_scopes_required(cls=None, value=None)  # type: ignore
    """
    with pytest.raises(ValueError):
        validate_scopes_required(
            cls=None, value=["read", "write", "execute"]
        )
    """


def test_validate_scopes_optional() -> None:
    assert validate_scopes_optional(cls=None, value=None) is None
    assert validate_scopes_optional(cls=None, value=["read:test", "write:test"]) == [
        AclPrivilege("read:test"),
        AclPrivilege("write:test"),
    ]
    assert validate_scopes_optional(
        cls=None, value=[AclPrivilege("read:test"), AclPrivilege("write:test")]
    ) == [
        AclPrivilege("read:test"),
        AclPrivilege("write:test"),
    ]
    assert validate_scopes_optional(cls=None, value=["read:test", "write:test"]) == [
        AclPrivilege("read:test"),
        AclPrivilege("write:test"),
    ]
    """
    with pytest.raises(ValueError):
        assert validate_scopes_optional(cls=None, value=["read", "write"])
    with pytest.raises(ValueError):
        assert validate_scopes_optional(cls=None, value=["read", AclPrivilege("write")])
    """
