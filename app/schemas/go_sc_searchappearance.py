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
class GoSearchConsoleSearchappearanceBase(
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


class GoSearchConsoleSearchappearanceCreate(GoSearchConsoleSearchappearanceBase):
    pass


class GoSearchConsoleSearchappearanceUpdate(BaseSchema):
    pass


class GoSearchConsoleSearchappearanceRead(
    GoSearchConsoleSearchappearanceBase,
    BaseSchemaRead,
):
    id: UUID4
