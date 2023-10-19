from __future__ import annotations

from typing import Optional

from pydantic import UUID4

from app.db.validators import (
    ValidateSchemaDescriptionOptional,
    ValidateSchemaTitleOptional,
    ValidateSchemaTitleRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class ClientBase(
    ValidateSchemaTitleRequired,
    ValidateSchemaDescriptionOptional,
):
    title: str
    description: Optional[str] = None
    is_active: Optional[bool] = True


class ClientCreate(ClientBase):
    title: str
    description: Optional[str] = None


class ClientUpdate(
    ValidateSchemaTitleOptional,
    ValidateSchemaDescriptionOptional,
):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ClientRead(ClientBase, BaseSchemaRead):
    id: UUID4
