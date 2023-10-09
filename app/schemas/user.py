from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4

from app.db.acls import UserACL
from app.db.validators import (
    ValidateSchemaAuthIdRequired,
    ValidateSchemaEmailRequired,
    ValidateSchemaUsernameOptional,
    ValidateSchemaUsernameRequired,
)
from app.schemas.base import BaseSchema, BaseSchemaRead
from app.schemas.user_roles import UserRole


# schemas
class UserBase(
    ValidateSchemaAuthIdRequired,
    ValidateSchemaEmailRequired,
    BaseSchema,
):
    auth_id: str
    email: str
    roles: List[UserRole] = [UserRole.USER]


class UserCreate(
    ValidateSchemaUsernameRequired,
    UserBase,
):
    username: str
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
    roles: Optional[List[UserRole]] = None


class UserRead(UserACL, UserBase, BaseSchemaRead):
    id: UUID4

    def principals(self) -> List[str]:
        return [f"user:{self.auth_id}"]


# relationships
class UserReadRelations(UserRead):
    clients: Optional[List["ClientRead"]] = []
    notes: Optional[List["NoteRead"]] = []


from app.schemas.client import ClientRead  # noqa: E402
from app.schemas.note import NoteRead  # noqa: E402

UserReadRelations.model_rebuild()