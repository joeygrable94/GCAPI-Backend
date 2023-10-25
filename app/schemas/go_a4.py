from __future__ import annotations

from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_measurement_id_required,
    validate_property_id_required,
    validate_title_optional,
    validate_title_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GoAnalytics4PropertyBase(BaseSchema):
    title: str
    measurement_id: str
    property_id: str
    client_id: UUID4
    website_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_measurement_id = field_validator("measurement_id", mode="before")(
        validate_measurement_id_required
    )
    _validate_property_id = field_validator("property_id", mode="before")(
        validate_property_id_required
    )


class GoAnalytics4PropertyCreate(GoAnalytics4PropertyBase):
    pass


class GoAnalytics4PropertyUpdate(BaseSchema):
    title: Optional[str] = None
    client_id: Optional[UUID4] = None
    website_id: Optional[UUID4] = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)


class GoAnalytics4PropertyRead(
    GoAnalytics4PropertyBase,
    BaseSchemaRead,
):
    id: UUID4
