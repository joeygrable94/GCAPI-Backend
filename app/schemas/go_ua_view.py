from __future__ import annotations

from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_title_optional,
    validate_title_required,
    validate_view_id_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GoAnalytics4ViewBase(BaseSchema):
    title: str
    view_id: str
    gua_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_view_id = field_validator("view_id", mode="before")(
        validate_view_id_required
    )


class GoUniversalAnalyticsViewCreate(GoAnalytics4ViewBase):
    pass


class GoUniversalAnalyticsViewUpdate(BaseSchema):
    title: Optional[str] = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)


class GoUniversalAnalyticsViewRead(
    GoAnalytics4ViewBase,
    BaseSchemaRead,
):
    id: UUID4
