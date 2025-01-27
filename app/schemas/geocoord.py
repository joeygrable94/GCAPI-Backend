from pydantic import UUID4, field_validator

from app.db.validators import validate_address_optional, validate_address_required
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GeocoordBase(BaseSchema):
    address: str
    latitude: float
    longitude: float

    _validate_address = field_validator("address", mode="before")(
        validate_address_required
    )


class GeocoordCreate(GeocoordBase):
    pass


class GeocoordUpdate(BaseSchema):
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    _validate_address = field_validator("address", mode="before")(
        validate_address_optional
    )


class GeocoordRead(GeocoordBase, BaseSchemaRead):
    id: UUID4
