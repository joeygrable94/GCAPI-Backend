from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4

from app.core.security.permissions import AclScope
from app.db.validators import (
    ValidateSchemaAuthIdRequired,
    ValidateSchemaEmailRequired,
    ValidateSchemaUsernameOptional,
    ValidateSchemaUsernameRequired,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class UserBase(
    ValidateSchemaAuthIdRequired,
    ValidateSchemaEmailRequired,
    BaseSchema,
):
    auth_id: str
    email: str
    roles: List[str] = ["role:user"]
    scopes: List[str] = []
    username: str


class UserCreate(
    ValidateSchemaUsernameRequired,
    UserBase,
):
    is_active: bool = True
    is_verified: bool = False
    is_superuser: bool = False


class UserUpdate(
    ValidateSchemaUsernameOptional,
    BaseSchema,
):
    username: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_superuser: Optional[bool] = None
    roles: Optional[List[str]] = None
    scopes: Optional[List[str]] = None


class UserRead(UserBase, BaseSchemaRead):
    id: UUID4
