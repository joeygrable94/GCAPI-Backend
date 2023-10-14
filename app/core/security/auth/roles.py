from enum import Enum


# schemas
class UserRole(Enum):
    USER = "user"  # default
    EMPLOYEE = "employee"
    MANAGER = "manager"
    CLIENT = "client"
    ADMIN = "admin"
