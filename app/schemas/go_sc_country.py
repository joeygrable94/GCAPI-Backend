from __future__ import annotations

from datetime import datetime

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_clicks_required,
    validate_impressions_required,
    validate_keys_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GoSearchConsoleCountryBase(BaseSchema):
    keys: str
    clicks: int
    impressions: int
    ctr: float
    position: float
    date_start: datetime
    date_end: datetime
    gsc_id: UUID4

    _validate_keys = field_validator("keys", mode="before")(validate_keys_required)
    _validate_clicks = field_validator("clicks", mode="before")(
        validate_clicks_required
    )
    _validate_impressions = field_validator("impressions", mode="before")(
        validate_impressions_required
    )


class GoSearchConsoleCountryCreate(GoSearchConsoleCountryBase):
    pass


class GoSearchConsoleCountryUpdate(BaseSchema):
    pass


class GoSearchConsoleCountryRead(
    GoSearchConsoleCountryBase,
    BaseSchemaRead,
):
    id: UUID4
