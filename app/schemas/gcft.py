from __future__ import annotations

from typing import Optional

from pydantic import UUID4

from app.db.validators import (
    ValidateGroupNameOptional,
    ValidateGroupNameRequired,
    ValidateGroupSlugRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class GcftBase(
    ValidateGroupNameRequired,
    ValidateGroupSlugRequired,
):
    group_name: str
    group_slug: str
    client_id: UUID4


class GcftCreate(GcftBase):
    pass


class GcftUpdate(
    ValidateGroupNameOptional,
):
    group_name: Optional[str] = None
    client_id: Optional[UUID4] = None


class GcftRead(GcftBase, BaseSchemaRead):
    id: UUID4
