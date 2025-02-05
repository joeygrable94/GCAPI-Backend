from pydantic import UUID4, field_validator

from app.core.schema import BaseSchema, BaseSchemaRead
from app.db.validators import (
    validate_group_name_optional,
    validate_group_name_required,
    validate_group_slug_required,
)


class GcftBase(BaseSchema):
    group_name: str
    group_slug: str
    organization_id: UUID4

    _validate_group_name = field_validator("group_name", mode="before")(
        validate_group_name_required
    )
    _validate_group_slug = field_validator("group_slug", mode="before")(
        validate_group_slug_required
    )


class GcftCreate(GcftBase):
    pass


class GcftUpdate(BaseSchema):
    group_name: str | None = None
    organization_id: UUID4 | None = None

    _validate_group_name = field_validator("group_name", mode="before")(
        validate_group_name_optional
    )


class GcftRead(GcftBase, BaseSchemaRead):
    id: UUID4
