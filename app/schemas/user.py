from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4

from app.db.acls import UserACL
from app.db.validators import (
    ValidateSchemaAuthIdRequired,
    ValidateSchemaUsernameOptional,
    ValidateSchemaUsernameRequired,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class UserBase(BaseSchema):
    is_active: bool = True
    is_verified: bool = False
    is_superuser: bool = False


class UserCreate(
    ValidateSchemaAuthIdRequired,
    ValidateSchemaUsernameRequired,
    UserBase,
):
    auth_id: str
    username: str


class UserUpdate(
    ValidateSchemaUsernameOptional,
    BaseSchema,
):
    username: Optional[str]
    is_active: Optional[bool]
    is_verified: Optional[bool]
    is_superuser: Optional[bool]


class UserRead(UserACL, UserBase, BaseSchemaRead):
    id: UUID4


# relationships
class UserReadRelations(UserRead):
    clients: Optional[List["ClientRead"]] = []
    notes: Optional[List["NoteRead"]] = []


from app.schemas.client import ClientRead  # noqa: E402
from app.schemas.note import NoteRead  # noqa: E402

UserReadRelations.update_forward_refs()
