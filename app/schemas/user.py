from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4, field_validator

from app.core.security.permissions import AclPrivilege
from app.db.validators import (
    validate_auth_id_required,
    validate_email_required,
    validate_scopes_optional,
    validate_scopes_required,
    validate_username_optional,
    validate_username_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class UserBase(BaseSchema):
    auth_id: str
    email: str
    username: str

    _validate_auth_id = field_validator("auth_id", mode="before")(
        validate_auth_id_required
    )
    _validate_email = field_validator("email", mode="before")(validate_email_required)
    _validate_username = field_validator("username", mode="before")(
        validate_username_required
    )


class UserCreate(UserBase):
    is_active: bool = True
    is_verified: bool = False
    is_superuser: bool = False
    scopes: List[AclPrivilege] = [AclPrivilege("role:user")]

    _validate_scopes = field_validator("scopes", mode="before")(
        validate_scopes_required
    )


class UserUpdate(BaseSchema):
    username: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None

    _validate_username = field_validator("username", mode="before")(
        validate_username_optional
    )


class UserUpdateAsManager(BaseSchema):
    scopes: Optional[List[AclPrivilege]] = None

    _validate_scopes = field_validator("scopes", mode="before")(
        validate_scopes_optional
    )


class UserUpdateAsAdmin(UserUpdateAsManager):
    is_superuser: Optional[bool] = None


class UserRead(UserBase, BaseSchemaRead):
    id: UUID4


class UserReadAsManager(
    UserBase,
    BaseSchemaRead,
):
    id: UUID4
    is_active: bool
    is_verified: bool
    scopes: List[AclPrivilege]

    _validate_scopes = field_validator("scopes", mode="before")(
        validate_scopes_required
    )


class UserReadAsAdmin(
    UserBase,
    BaseSchemaRead,
):
    id: UUID4
    is_active: bool
    is_verified: bool
    is_superuser: bool
    scopes: List[AclPrivilege]

    _validate_scopes = field_validator("scopes", mode="before")(
        validate_scopes_required
    )
