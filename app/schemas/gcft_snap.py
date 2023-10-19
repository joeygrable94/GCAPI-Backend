from __future__ import annotations

from typing import Optional

from pydantic import UUID4

from app.db.validators import (
    ValidateSchemaAltitudeOptional,
    ValidateSchemaAltitudeRequired,
    ValidateSchemaSnapNameOptional,
    ValidateSchemaSnapNameRequired,
    ValidateSchemaSnapSlugRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class GcftSnapBase(
    ValidateSchemaSnapNameRequired,
    ValidateSchemaSnapSlugRequired,
    ValidateSchemaAltitudeRequired,
):
    snap_name: str
    snap_slug: str
    altitude: int
    gcft_id: UUID4
    geocoord_id: UUID4
    file_asset_id: Optional[UUID4] = None


class GcftSnapCreate(GcftSnapBase):
    pass


class GcftSnapUpdate(
    ValidateSchemaSnapNameOptional,
    ValidateSchemaAltitudeOptional,
):
    snap_name: Optional[str] = None
    altitude: Optional[int] = None
    gcft_id: Optional[UUID4] = None
    geocoord_id: Optional[UUID4] = None
    file_asset_id: Optional[UUID4] = None


class GcftSnapRead(GcftSnapBase, BaseSchemaRead):
    id: UUID4
