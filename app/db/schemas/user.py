from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, EmailStr, validator

from app.core.config import settings
from app.core.utilities import scope_regex
from app.db.acls.user import UserACL
from app.db.schemas.base import BaseSchema, BaseSchemaRead


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


# schemas
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


class UserRead(UserACL, ValidateUserEmailRequired, BaseSchemaRead):
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserPrincipals(UserRead, ValidateUserPrincipals):
    principals: List[str]


# relationships
class UserReadRelations(UserRead):
    clients: Optional[List["ClientRead"]] = []


class AdminReadUserPrincipals(UserPrincipals):
    ip_addresses: Optional[List["IpAddressRead"]] = []
    tokens: Optional[List["AccessTokenRead"]] = []
    clients: Optional[List["ClientRead"]] = []


# import and update pydantic relationship refs
from app.db.schemas.accesstoken import AccessTokenRead  # noqa: E402
from app.db.schemas.client import ClientRead  # noqa: E402
from app.db.schemas.ipaddress import IpAddressRead  # noqa: E402

UserReadRelations.update_forward_refs()
AdminReadUserPrincipals.update_forward_refs()
