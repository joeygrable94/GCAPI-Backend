from __future__ import annotations

from datetime import datetime

from pydantic import UUID4

from app.db.validators import (
    ValidateSchemaClicksRequired,
    ValidateSchemaCtrRequired,
    ValidateSchemaImpressionsRequired,
    ValidateSchemaKeysRequired,
    ValidateSchemaPositionRequired,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GoSearchConsoleDeviceBase(
    ValidateSchemaKeysRequired,
    ValidateSchemaClicksRequired,
    ValidateSchemaImpressionsRequired,
    ValidateSchemaCtrRequired,
    ValidateSchemaPositionRequired,
):
    keys: str
    clicks: int
    impressions: int
    ctr: float
    position: float
    date_start: datetime
    date_end: datetime
    gsc_id: UUID4


class GoSearchConsoleDeviceCreate(GoSearchConsoleDeviceBase):
    pass


class GoSearchConsoleDeviceUpdate(BaseSchema):
    pass


class GoSearchConsoleDeviceRead(
    GoSearchConsoleDeviceBase,
    BaseSchemaRead,
):
    id: UUID4
