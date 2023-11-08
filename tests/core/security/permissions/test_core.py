import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.users import create_random_user

from app.core.security.permissions.core import (
    DENY_ALL,
    AclAction,
    AclPermission,
    AclPrivilege,
    has_permission,
    is_like_list,
    list_permissions,
    normalize_acl,
)
from app.models.user import User

pytestmark = pytest.mark.asyncio


async def test_list_permissions(db_session: AsyncSession) -> None:
    class Resource:
        __acl__ = [
            (AclAction.allow, AclPrivilege("role:user"), AclPermission("access:read")),
            (
                AclAction.allow,
                AclPrivilege("role:admin"),
                AclPermission("access:write"),
            ),
            (AclAction.deny, AclPrivilege("role:user"), AclPermission("access:delete")),
        ]

    resource = Resource()

    user_privileges = [AclPrivilege("role:user")]
    expected_permissions = {
        "access:read": True,
        "access:write": False,
        "access:delete": False,
    }
    actual_permissions = list_permissions(user_privileges, resource)
    assert actual_permissions == expected_permissions

    user_privileges = [AclPrivilege("role:admin")]
    expected_permissions = {
        AclPermission("access:read"): False,
        AclPermission("access:write"): True,
        AclPermission("access:delete"): False,
    }
    actual_permissions = list_permissions(user_privileges, resource)
    assert actual_permissions == expected_permissions

    user_privileges = [AclPrivilege("role:guest")]
    expected_permissions = {
        AclPermission("access:read"): False,
        AclPermission("access:write"): False,
        AclPermission("access:delete"): False,
    }
    actual_permissions = list_permissions(user_privileges, resource)
    assert actual_permissions == expected_permissions

    user_privileges = [AclPrivilege("role:user"), AclPrivilege("role:admin")]
    expected_permissions = {
        AclPermission("access:read"): True,
        AclPermission("access:write"): True,
        AclPermission("access:delete"): False,
    }
    actual_permissions = list_permissions(user_privileges, resource)
    assert actual_permissions == expected_permissions

    user_privileges = [AclPrivilege("role:guest"), AclPrivilege("role:admin")]
    expected_permissions = {
        AclPermission("access:read"): False,
        AclPermission("access:write"): True,
        AclPermission("access:delete"): False,
    }
    actual_permissions = list_permissions(user_privileges, resource)
    assert actual_permissions == expected_permissions

    user_privileges = [AclPrivilege("role:guest"), AclPrivilege("role:user")]
    expected_permissions = {
        AclPermission("access:read"): True,
        AclPermission("access:write"): False,
        AclPermission("access:delete"): False,
    }
    actual_permissions = list_permissions(user_privileges, resource)
    assert actual_permissions == expected_permissions

    user_privileges = [
        AclPrivilege("role:guest"),
        AclPrivilege("role:user"),
        AclPrivilege("role:admin"),
    ]
    expected_permissions = {
        AclPermission("access:read"): True,
        AclPermission("access:write"): True,
        AclPermission("access:delete"): False,
    }
    actual_permissions = list_permissions(user_privileges, resource)
    assert actual_permissions == expected_permissions


async def test_normalize_acl(db_session: AsyncSession) -> None:
    class Resource:
        __acl__ = [
            (AclAction.allow, AclPrivilege("role:user"), AclPermission("access:read"))
        ]

    resource = Resource()
    assert normalize_acl(resource) == [
        (AclAction.allow, AclPrivilege("role:user"), AclPermission("access:read"))
    ]

    resource = [
        (AclAction.allow, AclPrivilege("role:user"), AclPermission("access:read"))
    ]
    assert normalize_acl(resource) == [
        (AclAction.allow, AclPrivilege("role:user"), AclPermission("access:read"))
    ]

    resource = None
    assert normalize_acl(resource) == [DENY_ALL]

    resource: str = "abc"
    assert normalize_acl(resource) == [DENY_ALL]

    resource: int = 123
    assert normalize_acl(resource) == [DENY_ALL]

    resource: dict = {}
    assert normalize_acl(resource) == {}

    resource: set = set()
    assert normalize_acl(resource) == set()

    resource: tuple = ()
    assert normalize_acl(resource) == ()

    user: User = await create_random_user(db_session)
    normalized = normalize_acl(user)
    assert normalized == user.__acl__()


async def test_is_like_list() -> None:
    assert is_like_list([]) is True
    assert is_like_list(()) is True
    assert is_like_list({}) is True
    assert is_like_list(set()) is True
    assert is_like_list("abc") is False
    assert is_like_list(123) is False
    assert is_like_list(None) is False


async def test_has_permission(db_session: AsyncSession) -> None:
    class Resource:
        __acl__ = [
            (AclAction.allow, AclPrivilege("role:user"), AclPermission("access:read")),
            (
                AclAction.allow,
                AclPrivilege("role:admin"),
                AclPermission("access:write"),
            ),
            (AclAction.deny, AclPrivilege("role:user"), AclPermission("access:delete")),
        ]

    resource = Resource()

    user_privileges = [AclPrivilege("role:user")]
    requested_permission = AclPermission("access:read")
    assert has_permission(user_privileges, requested_permission, resource) is True

    user_privileges = [AclPrivilege("role:user")]
    requested_permission = AclPermission("access:write")
    assert has_permission(user_privileges, requested_permission, resource) is False

    user_privileges = [AclPrivilege("role:user")]
    requested_permission = AclPermission("access:delete")
    assert has_permission(user_privileges, requested_permission, resource) is False

    user_privileges = [AclPrivilege("role:admin")]
    requested_permission = AclPermission("access:read")
    assert has_permission(user_privileges, requested_permission, resource) is False

    user_privileges = [AclPrivilege("role:admin")]
    requested_permission = AclPermission("access:write")
    assert has_permission(user_privileges, requested_permission, resource) is True

    user_privileges = [AclPrivilege("role:admin")]
    requested_permission = AclPermission("access:delete")
    assert has_permission(user_privileges, requested_permission, resource) is False

    user_privileges = [AclPrivilege("role:guest")]
    requested_permission = AclPermission("access:read")
    assert has_permission(user_privileges, requested_permission, resource) is False

    user_privileges = [AclPrivilege("role:guest")]
    requested_permission = AclPermission("access:write")
    assert has_permission(user_privileges, requested_permission, resource) is False

    user_privileges = [AclPrivilege("role:guest")]
    requested_permission = AclPermission("access:delete")
    assert has_permission(user_privileges, requested_permission, resource) is False

    user_privileges = [AclPrivilege("role:user"), AclPrivilege("role:admin")]
    requested_permission = AclPermission("access:read")
    assert has_permission(user_privileges, requested_permission, resource) is True

    user_privileges = [AclPrivilege("role:user"), AclPrivilege("role:admin")]
    requested_permission = AclPermission("access:write")
    assert has_permission(user_privileges, requested_permission, resource) is True

    user_privileges = [AclPrivilege("role:user"), AclPrivilege("role:admin")]
    requested_permission = AclPermission("access:delete")
    assert has_permission(user_privileges, requested_permission, resource) is False

    user_privileges = [AclPrivilege("role:guest"), AclPrivilege("role:admin")]
    requested_permission = AclPermission("access:read")
    assert has_permission(user_privileges, requested_permission, resource) is False

    user_privileges = [AclPrivilege("role:guest"), AclPrivilege("role:admin")]
    requested_permission = AclPermission("access:write")
    assert has_permission(user_privileges, requested_permission, resource) is True

    user_privileges = [AclPrivilege("role:guest"), AclPrivilege("role:admin")]
    requested_permission = AclPermission("access:delete")
    assert has_permission(user_privileges, requested_permission, resource) is False

    user_privileges = [AclPrivilege("role:guest"), AclPrivilege("role:user")]
    requested_permission = AclPermission("access:read")
    assert has_permission(user_privileges, requested_permission, resource) is True

    user_privileges = [AclPrivilege("role:guest"), AclPrivilege("role:user")]
    requested_permission = AclPermission("access:write")
    assert has_permission(user_privileges, requested_permission, resource) is False

    user_privileges = [AclPrivilege("role:guest"), AclPrivilege("role:user")]
    requested_permission = AclPermission("access:delete")
    assert has_permission(user_privileges, requested_permission, resource) is False

    user_privileges = [
        AclPrivilege("role:guest"),
        AclPrivilege("role:user"),
        AclPrivilege("role:admin"),
    ]
    requested_permission = AclPermission("access:read")
    assert has_permission(user_privileges, requested_permission, resource) is True

    user_privileges = [
        AclPrivilege("role:guest"),
        AclPrivilege("role:user"),
        AclPrivilege("role:admin"),
    ]
    requested_permission = AclPermission("access:write")
    assert has_permission(user_privileges, requested_permission, resource) is True

    user_privileges = [
        AclPrivilege("role:guest"),
        AclPrivilege("role:user"),
        AclPrivilege("role:admin"),
    ]
    requested_permission = AclPermission("access:delete")
    assert has_permission(user_privileges, requested_permission, resource) is False
