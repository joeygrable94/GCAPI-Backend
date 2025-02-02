"""Row Level Permissions for FastAPI

Based on [FastAPI Permissions by @holgi](https://github.com/holgi/fastapi-permissions)


# Permission is already wrapped in Depends()
Permission = configure_permissions(get_active_user_principals)

@app.get("/item/{item_identifier}")
async def show_item(item: Item=Permission(AclPrivilege("read:item"), get_item)):
    return [{"item": item}]

"""

__version__ = "0.2.7"

import functools
from typing import Any

from fastapi import Depends

from .errors import AuthPermissionException
from .schemas import DENY_ALL, AclAction, AclPermission, AclPrivilege


def configure_permissions(
    active_privileges_func: Any,
) -> Any:
    """sets the basic configuration for the permissions system

    active_privileges_func:
        a dependency that returns the privileges of the current active user

    returns: permission_dependency_factory function,
             with some parameters already provisioned
    """
    active_privileges_func = Depends(active_privileges_func)

    return functools.partial(
        permission_dependency_factory,
        active_privileges_func=active_privileges_func,
    )


def permission_dependency_factory(
    permission: AclPermission | list[AclPermission],
    resource: Any,
    active_privileges_func: Any,
) -> Any:
    """returns a function that acts as a dependable for checking permissions

    This is the actual function used for creating the permission dependency,
    with the help of fucntools.partial in the "configure_permissions()"
    function.

    permission:
        the permission to check
    resource:
        the resource that will be accessed
    active_privileges_func (provisioned  by configure_permissions):
        a dependency that returns the privileges of the current active user

    returns: dependency function for "Depends()"
    """
    if callable(resource):
        dependable_resource = Depends(resource)
    else:
        dependable_resource = Depends(lambda: resource)  # pragma: no cover

    # to get the caller signature right, we need to add only the resource and
    # user dependable in the definition
    # the permission itself is available through the outer function scope
    def permission_dependency(
        resource: Any = dependable_resource,
        privileges: list[AclPrivilege] = active_privileges_func,
    ) -> Any:  # pragma: no cover
        if isinstance(permission, list):
            for perm in permission:
                if has_permission(privileges, perm, resource):
                    return resource
        else:
            if has_permission(privileges, permission, resource):
                return resource
        raise AuthPermissionException()

    return Depends(permission_dependency)


def has_permission(
    user_privileges: list[AclPrivilege],
    requested_permission: AclPermission,
    resource: Any,
) -> bool:
    """checks if a user has the permission for a resource

    The order of the function parameters can be remembered like "Joe eat apple"

    user_privileges: the privileges of a user
    requested_permission: the permission that should be checked
    resource: the object the user wants to access, must provide an ACL

    returns bool: permission granted or denied
    """
    acl = normalize_acl(resource)

    for action, privilege, permissions in acl:
        if requested_permission in permissions:
            if privilege in user_privileges:
                return action == AclAction.allow
    return False


def list_permissions(
    user_privileges: list[AclPrivilege], resource: Any
) -> dict[AclPermission, bool]:
    """lists all permissions of a user for a resouce

    user_privileges: the privileges of a user
    resource: the object the user wants to access, must provide an ACL

    returns dict: every available permission of the resource as key
                  and True / False as value if the permission is granted.
    """
    acl = normalize_acl(resource)

    acl_permissions = (permissions for _, _, permissions in acl)
    permissions = list(acl_permissions)

    return {p: has_permission(user_privileges, p, resource) for p in permissions}


def normalize_acl(
    resource: Any,
) -> list[tuple[AclAction, AclPrivilege, AclPermission]]:
    """returns the access controll list for a resource

    If the resource is not an acl list itself it needs to have an "__acl__"
    attribute. If the "__acl__" attribute is a callable, it will be called and
    the result of the call returned.

    An existing __acl__ attribute takes precedence before checking if it is an
    iterable.
    """
    acl = getattr(resource, "__acl__", None)
    if callable(acl):
        return acl()
    elif acl is not None:
        return acl
    elif is_like_list(resource):
        return resource
    return [DENY_ALL]


def is_like_list(something: Any) -> bool:
    """checks if something is iterable but not a string"""
    if isinstance(something, str):
        return False
    return hasattr(something, "__iter__")
