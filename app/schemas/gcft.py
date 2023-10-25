from __future__ import annotations

from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_group_name_optional,
    validate_group_name_required,
    validate_group_slug_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GcftBase(BaseSchema):
    group_name: str
    group_slug: str
    client_id: UUID4

    _validate_group_name = field_validator("group_name", mode="before")(
        validate_group_name_required
    )
    _validate_group_slug = field_validator("group_slug", mode="before")(
        validate_group_slug_required
    )


class GcftCreate(GcftBase):
    pass


class GcftUpdate(BaseSchema):
    group_name: Optional[str] = None
    client_id: Optional[UUID4] = None

    _validate_group_name = field_validator("group_name", mode="before")(
        validate_group_name_optional
    )


class GcftRead(GcftBase, BaseSchemaRead):
    id: UUID4
