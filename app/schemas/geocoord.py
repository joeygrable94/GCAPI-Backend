from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_address_optional,
    validate_address_required,
    validate_latitude_optional,
    validate_latitude_required,
    validate_longitude_optional,
    validate_longitude_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GeocoordBase(BaseSchema):
    address: str
    latitude: float
    longitude: float

    _validate_address = field_validator("address", mode="before")(
        validate_address_required
    )
    _validate_latitude = field_validator("latitude", mode="before")(
        validate_latitude_required
    )
    _validate_longitude = field_validator("longitude", mode="before")(
        validate_longitude_required
    )


class GeocoordCreate(GeocoordBase):
    pass


class GeocoordUpdate(BaseSchema):
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    _validate_address = field_validator("address", mode="before")(
        validate_address_optional
    )
    _validate_latitude = field_validator("latitude", mode="before")(
        validate_latitude_optional
    )
    _validate_longitude = field_validator("longitude", mode="before")(
        validate_longitude_optional
    )


class GeocoordRead(GeocoordBase, BaseSchemaRead):
    id: UUID4
