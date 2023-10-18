"""Row Level Permissions for FastAPI

Based on [FastAPI Permissions by @holgi](https://github.com/holgi/fastapi-permissions)

This module provides an implementation for row level permissions for the
FastAPI framework. This is heavily inspired / ripped off the Pyramids Web
Framework, so all cudos to them!

extremely simple and incomplete example:

    from fastapi import Depends, FastAPI
    from fastapi.security import OAuth2PasswordBearer
    from pydantic import BaseModel

    from permissions import import configure_permissions, AclAction, AclPermission

    app = FastAPI()
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

    class Item(BaseModel):
        name: str
        owner: str

        def __acl__(self):
            return [
                (AclAction.allow, Authenticated, AclPermission.read),
                (AclAction.allow, "role:admin", AclPermission.update),
                (AclAction.allow, f"user:{self.owner}", AclPermission.delete),
            ]

    class User(BaseModel):
        name: str

        def privileges(self):
            return [f"user:{self.name}"]

    def get_current_user(token: str = Depends(oauth2_scheme)):
        ...

    def get_active_user_privileges(user:User = Depends(get_current_user)):
        ...

    def get_item(item_identifier):
        ...

    # Permission is already wrapped in Depends()
    Permissions = configure_permissions(get_active_user_privileges)

    @app.get("/item/{item_identifier}")
    async def show_item(item:Item = Permission("view", get_item)):
        return [{"item": item}]
"""

__version__ = "0.2.7"

import functools
from enum import StrEnum
from typing import Any, Dict, List, NewType, Tuple

from fastapi import Depends, HTTPException

from .exceptions import permission_exception

# constants


# Action
class AclAction(StrEnum):
    allow = "allow"
    deny = "deny"


# Privileges
AclPrivilege = NewType("AclPrivilege", str)
Everyone: AclPrivilege = AclPrivilege("system:everyone")
Authenticated: AclPrivilege = AclPrivilege("system:authenticated")


# Permissions
class AclPermission(StrEnum):
    all: str = "permission:*"
    create: str = "permission:create"
    read: str = "permission:read"
    update: str = "permission:update"
    delete: str = "permission:delete"
    read_relations: str = "permission:read_relations"


# ACL Tuples: Action, Privilege, Permission
DENY_ALL: Tuple[AclAction, AclPrivilege, AclPermission] = (
    AclAction.deny,
    Everyone,
    AclPermission.all,
)
ALOW_ALL: Tuple[AclAction, AclPrivilege, AclPermission] = (
    AclAction.allow,
    Everyone,
    AclPermission.all,
)


def configure_permissions(
    active_privileges_func: Any,
    permission_exception: HTTPException = permission_exception,
) -> Any:
    """sets the basic configuration for the permissions system

    active_privileges_func:
        a dependency that returns the privileges of the current active user
    permission_exception:
        the exception used if a permission is denied

    returns: permission_dependency_factory function,
             with some parameters already provisioned
    """
    active_privileges_func = Depends(active_privileges_func)

    return functools.partial(
        permission_dependency_factory,
        active_privileges_func=active_privileges_func,
        permission_exception=permission_exception,
    )


def permission_dependency_factory(
    permission: AclPermission,
    resource: Any,
    active_privileges_func: Any,
    permission_exception: HTTPException,
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
    permission_exception (provisioned  by configure_permissions):
        exception if permission is denied

    returns: dependency function for "Depends()"
    """
    if callable(resource):
        dependable_resource = Depends(resource)
    else:
        dependable_resource = Depends(lambda: resource)

    # to get the caller signature right, we need to add only the resource and
    # user dependable in the definition
    # the permission itself is available through the outer function scope
    def permission_dependency(
        resource: Any = dependable_resource,
        privileges: Any = active_privileges_func,
    ) -> Any:
        if has_permission(privileges, permission, resource):
            return resource
        raise permission_exception

    return Depends(permission_dependency)


def has_permission(
    user_privileges: List[AclPrivilege],
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
    user_privileges: List[AclPrivilege], resource: Any
) -> Dict[AclPermission, bool]:
    """lists all permissions of a user for a resouce

    user_privileges: the privileges of a user
    resource: the object the user wants to access, must provide an ACL

    returns dict: every available permission of the resource as key
                  and True / False as value if the permission is granted.
    """
    acl = normalize_acl(resource)

    acl_permissions = (permissions for _, _, permissions in acl)
    permissions = list(acl_permissions)

    return {
        AclPermission[str(p)]: has_permission(user_privileges, p, resource)
        for p in permissions
    }


# utility functions


def normalize_acl(resource: Any) -> List[Tuple[AclAction, AclPrivilege, AclPermission]]:
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
