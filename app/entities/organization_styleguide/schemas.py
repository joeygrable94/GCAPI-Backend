from datetime import datetime

from pydantic import UUID4, field_validator

from app.core.schema import BaseSchema, BaseSchemaRead
from app.db.validators import (
    validate_description_optional,
    validate_styleguide_optional,
    validate_title_optional,
    validate_title_required,
    validate_url_optional,
)


class OrganizationStyleguideBase(BaseSchema):
    title: str
    description: str | None = None
    styleguide: str | None = None
    url: str | None
    is_active: bool = True
    organization_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )
    _validate_styleguide = field_validator("styleguide", mode="before")(
        validate_styleguide_optional
    )
    _validate_url = field_validator("url", mode="before")(validate_url_optional)


class OrganizationStyleguideCreate(OrganizationStyleguideBase):
    pass


class OrganizationStyleguideUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None
    styleguide: str | None = None
    url: str | None = None
    organization_id: UUID4 | None = None
    created: datetime | None = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )
    _validate_styleguide = field_validator("styleguide", mode="before")(
        validate_styleguide_optional
    )
    _validate_url = field_validator("url", mode="before")(validate_url_optional)


class OrganizationStyleguideRead(OrganizationStyleguideBase, BaseSchemaRead):
    id: UUID4
