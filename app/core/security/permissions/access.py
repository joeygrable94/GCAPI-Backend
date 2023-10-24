from .scope import AclPermission, AclScope

# Privileges
# generic
Everyone: AclScope = AclScope("system:everyone")
Authenticated: AclScope = AclScope("system:authenticated")
# role based privileges: client, employee, manager, user
RoleAdmin: AclScope = AclScope("role:admin")
RoleClient: AclScope = AclScope("role:client")
RoleEmployee: AclScope = AclScope("role:employee")
RoleManager: AclScope = AclScope("role:manager")
RoleUser: AclScope = AclScope("role:user")


# Permissions
# generic
AccessAll: AclPermission = AclPermission("access:all")
# list
AccessList: AclPermission = AclPermission("list:all")
AccessListRelated: AclPermission = AclPermission("list:related")
# create
AccessCreate: AclPermission = AclPermission("create:all")
# read
AccessRead: AclPermission = AclPermission("read:all")
AccessReadSelf: AclPermission = AclPermission("read:self")
AccessReadRelated: AclPermission = AclPermission("read:related")
# update
AccessUpdate: AclPermission = AclPermission("update:all")
AccessUpdateSelf: AclPermission = AclPermission("update:self")
# delete
AccessDelete: AclPermission = AclPermission("delete:all")
AccessDeleteSelf: AclPermission = AclPermission("delete:self")
