from .scope import AclPermission, AclPrivilege

# Privileges
# generic
Everyone: AclPrivilege = AclPrivilege("system:everyone")
Authenticated: AclPrivilege = AclPrivilege("system:authenticated")
# role based privileges: client, employee, manager, user
RoleAdmin: AclPrivilege = AclPrivilege("role:admin")
RoleClient: AclPrivilege = AclPrivilege("role:client")
RoleEmployee: AclPrivilege = AclPrivilege("role:employee")
RoleManager: AclPrivilege = AclPrivilege("role:manager")
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
