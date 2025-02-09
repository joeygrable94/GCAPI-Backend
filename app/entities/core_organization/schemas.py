from pydantic import UUID4, field_validator

from app.core.schema import BaseSchema, BaseSchemaRead
from app.db.validators import (
    validate_description_optional,
    validate_slug_required,
    validate_title_optional,
    validate_title_required,
)


class OrganizationBase(BaseSchema):
    slug: str
    title: str
    description: str | None = None
    is_active: bool = True

    _validate_slug = field_validator("slug", mode="before")(validate_slug_required)
    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )


class OrganizationCreate(OrganizationBase):
    title: str
    description: str | None = None
    is_active: bool = True


class OrganizationUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None
    is_active: bool | None = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )


class OrganizationRead(OrganizationBase, BaseSchemaRead):
    id: UUID4


class OrganizationReadPublic(BaseSchema):
    id: UUID4
    title: str


class OrganizationDelete(BaseSchema):
    message: str
    user_id: UUID4
    organization_id: UUID4
