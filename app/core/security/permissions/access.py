from .scope import Scope

# Privileges
# generic
Everyone: Scope = Scope("system:everyone")
Authenticated: Scope = Scope("system:authenticated")
# role based privileges: client, employee, manager, user
RoleAdmin: Scope = Scope("role:admin")
RoleClient: Scope = Scope("role:client")
RoleEmployee: Scope = Scope("role:employee")
RoleManager: Scope = Scope("role:manager")
RoleUser: Scope = Scope("role:user")


# Permissions
# generic
AccessAll: Scope = Scope("access:all")
# list
AccessList: Scope = Scope("list:all")
AccessListRelated: Scope = Scope("list:related")
# create
AccessCreate: Scope = Scope("create:all")
# read
AccessRead: Scope = Scope("read:all")
AccessReadSelf: Scope = Scope("read:self")
AccessReadRelated: Scope = Scope("read:related")
# update
AccessUpdate: Scope = Scope("update:all")
AccessUpdateSelf: Scope = Scope("update:self")
# delete
AccessDelete: Scope = Scope("delete:all")
AccessDeleteSelf: Scope = Scope("delete:self")
