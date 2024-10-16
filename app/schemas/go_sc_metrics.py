from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_clicks_optional,
    validate_clicks_required,
    validate_impressions_optional,
    validate_impressions_required,
    validate_keys_optional,
    validate_keys_required,
    validate_title_optional,
    validate_title_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GoSearchConsoleMetricType(str, Enum):
    searchappearance = "searchappearance"
    query = "query"
    page = "page"
    device = "device"
    country = "country"


class GoSearchConsoleMetricBase(BaseSchema):
    title: str
    keys: str
    clicks: int
    impressions: int
    ctr: float
    position: float
    date_start: datetime
    date_end: datetime
    gsc_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_keys = field_validator("keys", mode="before")(validate_keys_required)
    _validate_clicks = field_validator("clicks", mode="before")(
        validate_clicks_required
    )
    _validate_impressions = field_validator("impressions", mode="before")(
        validate_impressions_required
    )


class GoSearchConsoleMetricCreate(GoSearchConsoleMetricBase):
    pass


class GoSearchConsoleMetricUpdate(BaseSchema):
    title: str | None = None
    keys: str | None = None
    clicks: int | None = None
    impressions: int | None = None
    ctr: float | None = None
    position: float | None = None
    date_start: datetime | None = None
    date_end: datetime | None = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)
    _validate_keys = field_validator("keys", mode="before")(validate_keys_optional)
    _validate_clicks = field_validator("clicks", mode="before")(
        validate_clicks_optional
    )
    _validate_impressions = field_validator("impressions", mode="before")(
        validate_impressions_optional
    )


class GoSearchConsoleMetricRead(
    GoSearchConsoleMetricBase,
    BaseSchemaRead,
):
    id: UUID4


# paginated schemas


class GoSearchConsoleMetricPages(BaseSchema):
    searchappearance: Dict[str, Any] | None = None
    query: Dict[str, Any] | None = None
    page: Dict[str, Any] | None = None
    device: Dict[str, Any] | None = None
    country: Dict[str, Any] | None = None
