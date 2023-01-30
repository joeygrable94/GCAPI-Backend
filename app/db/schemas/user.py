from typing import Any, List, Optional, Tuple

from fastapi_permissions import Allow, Authenticated
from pydantic import BaseModel, EmailStr, validator

from app.core.config import settings
from app.core.utilities import scope_regex
from app.db.schemas.base import BaseSchema, BaseSchemaRead


# ACL
class UserACL(BaseSchema):
    def __acl__(self) -> List[Tuple[Any, Any, Any]]:
        """Defines who can do what.

        Returns a list of tuples (1, 2, 3):
            1. access level:
                Allow
                Deny
            2. principal identifier:
                Everyone
                Authenticated
                role:admin
                role:user
            3. permissions:
                super
                self
                list
                create
                read
                update
                delete

        If a role is not listed (like "role:user") the access will be
        automatically denied, as if (Deny, Everyone, All) is appended.
        """
        return [
            (Allow, Authenticated, "self"),
            (Allow, "role:admin", "list"),
            (Allow, "role:admin", "create"),
            (Allow, "role:admin", "read"),
            (Allow, "role:admin", "update"),
            (Allow, "role:admin", "delete"),
            (Allow, f"user:{settings.FIRST_SUPERUSER}", "super"),
            (Allow, f"user:{self.email}", "self"),  # type: ignore
        ]


# validators
class ValidateUserEmailRequired(BaseSchema):
    email: EmailStr

    @validator("email")
    def limits_email(cls, v: EmailStr) -> EmailStr:
        if len(v) < 6:
            raise ValueError("emails must contain 5 or more characters")
        if len(v) > 255:  # pragma: no cover
            raise ValueError("emails must contain less than 255 characters")
        if settings.EMAIL_PROVIDER_RESTRICTION:
            if not any(
                provider in v for provider in settings.ALLOWED_EMAIL_PROVIDER_LIST
            ):
                raise ValueError("invalid email provider")
        return EmailStr(v)


class ValidateUserEmailOptional(BaseSchema):
    email: Optional[EmailStr]

    @validator("email")
    def limits_email(cls, v: Optional[EmailStr]) -> Optional[EmailStr]:
        if v and len(v) < 6:
            raise ValueError("emails must contain 5 or more characters")
        if v and len(v) > 255:  # pragma: no cover
            raise ValueError("emails must contain less than 255 characters")
        if v and settings.EMAIL_PROVIDER_RESTRICTION:
            if not any(
                provider in v for provider in settings.ALLOWED_EMAIL_PROVIDER_LIST
            ):
                raise ValueError("invalid email provider")
        return v


class ValidateUserPrincipals(BaseModel):
    principals: List[str]

    @validator("principals")
    def validate_permission_scopes(cls, v: List[str]) -> List[str]:
        assert isinstance(v, list)
        for s in v:
            if not scope_regex.fullmatch(s.lower()):
                raise ValueError("invalid permission scope format")
        return v


class UserInDB(BaseSchema):
    email: EmailStr
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    principals: List[str]


class RequestUserCreate(ValidateUserEmailRequired):
    email: EmailStr
    password: str


class UserCreate(RequestUserCreate):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(ValidateUserEmailOptional):
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]


class UserUpdateAuthPermissions(ValidateUserEmailRequired, ValidateUserPrincipals):
    email: EmailStr
    principals: List[str]


class UserRead(UserACL, BaseSchemaRead, ValidateUserEmailRequired):
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserAdmin(UserRead, ValidateUserPrincipals):
    principals: List[str]
