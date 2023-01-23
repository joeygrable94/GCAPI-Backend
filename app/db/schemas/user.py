from typing import Any, List, Optional, Tuple

from fastapi_permissions import Allow, Authenticated
from pydantic import EmailStr

from app.db.schemas.base import BaseSchema, BaseSchemaRead


class UserInDB(BaseSchema):
    email: EmailStr
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    principals: List[str]


class RequestUserCreate(BaseSchema):
    email: EmailStr
    password: str


class UserCreate(BaseSchema):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(BaseSchema):
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]


class UserUpdateAuthPermissions(BaseSchema):
    email: Optional[EmailStr]
    principals: List[str]


class UserRead(BaseSchemaRead):
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool

    def __acl__(self) -> List[Tuple[Any, Any, Any]]:
        """Defines who can do what.

        Returns a list of tuples (1, 2, 3):
            1. "Allow" or "Deny"
            2. principal identifier: "scope:spec"
            3. permission name:
                "use", "list", "create", "read", "update", "delete", "self"

        If a role is not listed (like "role:user") the access will be
        automatically denied, as if (Deny, Everyone, All) is appended.
        """
        return [
            (Allow, Authenticated, "self"),
            (Allow, "role:admin", "use"),
            (Allow, "role:admin", "list"),
            (Allow, "role:admin", "create"),
            (Allow, "role:admin", "read"),
            (Allow, "role:admin", "update"),
            (Allow, "role:admin", "delete"),
            (Allow, f"user:{self.email}", "self"),
        ]


class UserReadAdmin(UserRead):
    principals: List[str]
