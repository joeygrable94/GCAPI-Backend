from __future__ import annotations

from typing import Optional

from pydantic import UUID4

from app.db.validators import (
    ValidateSchemaTitleOptional,
    ValidateSchemaTitleRequired,
    ValidateSchemaViewIdRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class GoAnalytics4ViewBase(
    ValidateSchemaTitleRequired,
    ValidateSchemaViewIdRequired,
):
    title: str
    view_id: str
    gua_id: UUID4


class GoUniversalAnalyticsViewCreate(GoAnalytics4ViewBase):
    pass


class GoUniversalAnalyticsViewUpdate(
    ValidateSchemaTitleOptional,
):
    title: Optional[str] = None


class GoUniversalAnalyticsViewRead(
    GoAnalytics4ViewBase,
    BaseSchemaRead,
):
    id: UUID4
