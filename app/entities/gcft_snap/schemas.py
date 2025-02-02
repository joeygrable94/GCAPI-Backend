from pydantic import UUID4, field_validator

from app.core.schema import BaseSchema, BaseSchemaRead
from app.db.validators import (
    validate_altitude_optional,
    validate_altitude_required,
    validate_snap_name_optional,
    validate_snap_name_required,
    validate_snap_slug_required,
)


class GcftSnapBase(BaseSchema):
    snap_name: str
    snap_slug: str
    altitude: int
    gcft_id: UUID4
    geocoord_id: UUID4
    file_asset_id: UUID4 | None = None

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
    snap_name: str | None = None
    altitude: int | None = None
    gcft_id: UUID4 | None = None
    geocoord_id: UUID4 | None = None
    file_asset_id: UUID4 | None = None

    _validate_snap_name = field_validator("snap_name", mode="before")(
        validate_snap_name_optional
    )
    _validate_altitude = field_validator("altitude", mode="before")(
        validate_altitude_optional
    )


class GcftSnapRead(GcftSnapBase, BaseSchemaRead):
    id: UUID4
