from __future__ import annotations

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
    scopes: list[AclPrivilege] = [AclPrivilege("role:user")]

    _validate_scopes = field_validator("scopes", mode="before")(
        validate_scopes_required
    )


class UserUpdate(BaseSchema):
    username: str | None = None

    _validate_username = field_validator("username", mode="before")(
        validate_username_optional
    )


class UserUpdateAsManager(BaseSchema):
    username: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None

    _validate_username = field_validator("username", mode="before")(
        validate_username_optional
    )


class UserUpdateAsAdmin(BaseSchema):
    username: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    is_superuser: bool | None = None

    _validate_username = field_validator("username", mode="before")(
        validate_username_optional
    )


class UserUpdatePrivileges(BaseSchema):
    scopes: list[AclPrivilege] | None = None

    _validate_scopes = field_validator("scopes", mode="before")(
        validate_scopes_optional
    )


class UserRead(UserBase, BaseSchemaRead):
    id: UUID4


class UserReadAsManager(UserBase, BaseSchemaRead):
    id: UUID4
    is_active: bool
    is_verified: bool
    scopes: list[AclPrivilege]

    _validate_scopes = field_validator("scopes", mode="before")(
        validate_scopes_required
    )


class UserReadAsAdmin(UserBase, BaseSchemaRead):
    id: UUID4
    is_active: bool
    is_verified: bool
    is_superuser: bool
    scopes: list[AclPrivilege]

    _validate_scopes = field_validator("scopes", mode="before")(
        validate_scopes_required
    )


class UserDelete(BaseSchema):
    message: str
    user_id: UUID4
    task_id: UUID4 | None = None
