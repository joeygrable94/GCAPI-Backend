from __future__ import annotations

from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_altitude_optional,
    validate_altitude_required,
    validate_snap_name_optional,
    validate_snap_name_required,
    validate_snap_slug_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GcftSnapBase(BaseSchema):
    snap_name: str
    snap_slug: str
    altitude: int
    gcft_id: UUID4
    geocoord_id: UUID4
    file_asset_id: Optional[UUID4] = None

    _validate_snap_name = field_validator("snap_name", mode="before")(
        validate_snap_name_required
    )
    _validate_snap_slug = field_validator("snap_slug", mode="before")(
        validate_snap_slug_required
    )
    _validate_altitude = field_validator("altitude", mode="before")(
        validate_altitude_required
    )


class GcftSnapCreate(GcftSnapBase):
    pass


class GcftSnapUpdate(BaseSchema):
    snap_name: Optional[str] = None
    altitude: Optional[int] = None
    gcft_id: Optional[UUID4] = None
    geocoord_id: Optional[UUID4] = None
    file_asset_id: Optional[UUID4] = None

    _validate_snap_name = field_validator("snap_name", mode="before")(
        validate_snap_name_optional
    )
    _validate_altitude = field_validator("altitude", mode="before")(
        validate_altitude_optional
    )


class GcftSnapRead(GcftSnapBase, BaseSchemaRead):
    id: UUID4
