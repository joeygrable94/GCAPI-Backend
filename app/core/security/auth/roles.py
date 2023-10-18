from enum import StrEnum


# schemas
class UserRole(StrEnum):
    user = "role:user"
    employee = "role:employee"
    manager = "role:manager"
    client = "role:client"
    admin = "role:admin"
