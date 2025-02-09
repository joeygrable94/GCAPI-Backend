# GCAPI Permission Concepts

- [FastAPI Permissions](https://github.com/holgi/fastapi-permissions?tab=readme-ov-file)
- [Pyramid ACL Security Docs](https://docs.pylonsproject.org/projects/pyramid/en/latest/api/authorization.html#pyramid.authorization.ACLHelper)

## Attribute Based Access Control

- input schemas
- output schemas
- paginated schemas

## Access Control Lists

The system depends on a couple of concepts not found in FastAPI:

- resources: objects that provide an access controll list
- access controll lists: a list of rules defining which principal has what permission
- principal: an identifier of a user or his/her associated groups/roles
- permission: an identifier (string) for an action on an object

A resource provides an access controll list via it's __acl__ attribute. It can either be a
property of an object or a callable. Each entry in the list is a tuple containing three values:

- an action: fastapi_permissions.Allow or fastapi_permissions.Deny
- a principal: e.g. "role:admin" or "user:bob"
- a permission or a tuple thereof: e.g. "edit" or ("view", "delete")
