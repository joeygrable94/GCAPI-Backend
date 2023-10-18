from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4

from app.db.validators import (
    ValidateSchemaTitleOptional,
    ValidateSchemaTitleRequired,
    ValidateSchemaTrackingIdRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class GoUniversalAnalytics4PropertyBase(
    ValidateSchemaTitleRequired,
    ValidateSchemaTrackingIdRequired,
):
    title: str
    tracking_id: str
    client_id: UUID4
    website_id: UUID4


class GoUniversalAnalyticsPropertyCreate(GoUniversalAnalytics4PropertyBase):
    pass


class GoUniversalAnalyticsPropertyUpdate(
    ValidateSchemaTitleOptional,
):
    title: Optional[str] = None
    client_id: Optional[UUID4] = None
    website_id: Optional[UUID4] = None


class GoUniversalAnalyticsPropertyRead(
    GoUniversalAnalytics4PropertyBase,
    BaseSchemaRead,
):
    id: UUID4


# relationships
class GoUniversalAnalyticsPropertyReadRelations(GoUniversalAnalyticsPropertyRead):
    gua_views: Optional[List["GoUniversalAnalyticsViewRead"]] = []


from app.schemas.go_ua_view import GoUniversalAnalyticsViewRead  # noqa: E402

GoUniversalAnalyticsPropertyReadRelations.model_rebuild()
