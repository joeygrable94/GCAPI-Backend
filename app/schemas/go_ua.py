from __future__ import annotations

from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_title_optional,
    validate_title_required,
    validate_tracking_id_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GoUniversalAnalytics4PropertyBase(BaseSchema):
    title: str
    tracking_id: str
    client_id: UUID4
    website_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_tracking_id = field_validator("tracking_id", mode="before")(
        validate_tracking_id_required
    )


class GoUniversalAnalyticsPropertyCreate(GoUniversalAnalytics4PropertyBase):
    pass


class GoUniversalAnalyticsPropertyUpdate(BaseSchema):
    title: Optional[str] = None
    client_id: Optional[UUID4] = None
    website_id: Optional[UUID4] = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)


class GoUniversalAnalyticsPropertyRead(
    GoUniversalAnalytics4PropertyBase,
    BaseSchemaRead,
):
    id: UUID4
