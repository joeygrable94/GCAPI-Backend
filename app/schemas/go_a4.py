from __future__ import annotations

from typing import Optional

from pydantic import UUID4

from app.db.validators import (
    ValidateSchemaMeasurementIdRequired,
    ValidateSchemaPropertyIdRequired,
    ValidateSchemaTitleOptional,
    ValidateSchemaTitleRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class GoAnalytics4PropertyBase(
    ValidateSchemaTitleRequired,
    ValidateSchemaMeasurementIdRequired,
    ValidateSchemaPropertyIdRequired,
):
    title: str
    measurement_id: str
    property_id: str
    client_id: UUID4
    website_id: UUID4


class GoAnalytics4PropertyCreate(GoAnalytics4PropertyBase):
    pass


class GoAnalytics4PropertyUpdate(
    ValidateSchemaTitleOptional,
):
    title: Optional[str] = None
    client_id: Optional[UUID4] = None
    website_id: Optional[UUID4] = None


class GoAnalytics4PropertyRead(
    GoAnalytics4PropertyBase,
    BaseSchemaRead,
):
    id: UUID4
