from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_property_id_required,
    validate_title_optional,
    validate_title_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GoAnalytics4PropertyBase(BaseSchema):
    title: str
    property_id: str
    client_id: UUID4
    platform_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_property_id = field_validator("property_id", mode="before")(
        validate_property_id_required
    )


class GoAnalytics4PropertyCreate(GoAnalytics4PropertyBase):
    pass


class RequestGoAnalytics4PropertyCreate(GoAnalytics4PropertyBase):
    title: str
    property_id: str
    client_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_property_id = field_validator("property_id", mode="before")(
        validate_property_id_required
    )


class GoAnalytics4PropertyUpdate(BaseSchema):
    title: str | None = None
    client_id: UUID4 | None = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)


class GoAnalytics4PropertyRead(GoAnalytics4PropertyBase, BaseSchemaRead):
    id: UUID4
