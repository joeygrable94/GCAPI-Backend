from enum import StrEnum
from typing import NewType


class AclAction(StrEnum):
    allow = "allow"
    deny = "deny"

    def __repr__(self) -> str:  # pragma: no cover
        return f"action:{self.value}"


Scope = NewType("Scope", str)
AclPermission = NewType("AclPermission", str)
AclPrivilege = NewType("AclPrivilege", str)


# Privileges
# generic
Everyone: AclPrivilege = AclPrivilege("system:everyone")
Authenticated: AclPrivilege = AclPrivilege("system:authenticated")
# role based privileges: client, employee, manager, user
RoleAdmin: AclPrivilege = AclPrivilege("role:admin")
RoleManager: AclPrivilege = AclPrivilege("role:manager")
RoleClient: AclPrivilege = AclPrivilege("role:client")
RoleEmployee: AclPrivilege = AclPrivilege("role:employee")
RoleUser: AclPrivilege = AclPrivilege("role:user")


# Permissions
# generic
AccessAll: AclPermission = AclPermission("access:all")
# list
AccessList: AclPermission = AclPermission("list:all")
AccessListSelf: AclPermission = AclPermission("list:self")
AccessListRelated: AclPermission = AclPermission("list:related")
# create
AccessCreate: AclPermission = AclPermission("create:all")
AccessCreateRelated: AclPermission = AclPermission("create:related")
# read
AccessRead: AclPermission = AclPermission("read:all")
AccessReadSelf: AclPermission = AclPermission("read:self")
AccessReadRelated: AclPermission = AclPermission("read:related")
# update
AccessUpdate: AclPermission = AclPermission("update:all")
AccessUpdateSelf: AclPermission = AclPermission("update:self")
AccessUpdateRelated: AclPermission = AclPermission("update:related")
# delete
AccessDelete: AclPermission = AclPermission("delete:all")
AccessDeleteSelf: AclPermission = AclPermission("delete:self")
AccessDeleteRelated: AclPermission = AclPermission("delete:related")


# Access Control Lists
# generic
DENY_ALL: tuple[AclAction, AclPrivilege, AclPermission] = (
    AclAction.deny,
    Everyone,
    AccessAll,
)
ALOW_ALL: tuple[AclAction, AclPrivilege, AclPermission] = (
    AclAction.allow,
    Everyone,
    AccessAll,
)
