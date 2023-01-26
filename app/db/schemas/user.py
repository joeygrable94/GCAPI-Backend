from typing import Any, List, Optional, Tuple

from fastapi_permissions import Allow, Authenticated
from pydantic import EmailStr, validator

from app.core.config import settings
from app.core.utilities import scope_regex
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

    @validator("email")
    def limits_email(cls, v: str) -> str:
        if len(v) < 5:
            raise ValueError("emails must contain 5 or more characters")
        if len(v) > 255:
            raise ValueError("emails must contain less than 255 characters")
        return v


class UserCreate(RequestUserCreate):
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

    @validator("email")
    def limits_email(cls, v: str) -> str:
        if v and len(v) < 5:
            raise ValueError("emails must contain 5 or more characters")
        if v and len(v) > 255:
            raise ValueError("emails must contain less than 255 characters")
        return v


class UserUpdateAuthPermissions(BaseSchema):
    email: EmailStr
    principals: List[str]

    @validator("principals")
    def validate_permission_scopes(cls, v: List[str]) -> List[str]:
        assert isinstance(v, list)
        for s in v:
            if not scope_regex.fullmatch(s.lower()):
                raise ValueError("invalid permission scope format")  # pragma: no cover
        return v


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
            (Allow, f"user:{settings.FIRST_SUPERUSER}", "super"),
            (Allow, f"user:{self.email}", "self"),
        ]


class UserAdmin(UserRead):
    principals: List[str]
