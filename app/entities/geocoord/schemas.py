from pydantic import UUID4, field_validator

from app.core.schema import BaseSchema, BaseSchemaRead
from app.db.validators import validate_address_optional


class GeocoordBase(BaseSchema):
    address: str | None
    latitude: float
    longitude: float

    _validate_address = field_validator("address", mode="before")(
        validate_address_optional
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
