from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4

from app.db.acls import GcftACL
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


class GcftRead(GcftACL, GcftBase, BaseSchemaRead):
    id: UUID4


# relationships
class GcftReadRelations(GcftRead):
    snaps: Optional[List["GcftSnapRead"]] = []


from app.schemas.gcft_snap import GcftSnapRead  # noqa: E402

GcftReadRelations.model_rebuild()
