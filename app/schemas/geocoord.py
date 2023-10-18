from typing import Optional

from pydantic import UUID4

from app.db.validators import (
    ValidateSchemaAddressOptional,
    ValidateSchemaAddressRequired,
    ValidateSchemaLatitudeOptional,
    ValidateSchemaLatitudeRequired,
    ValidateSchemaLongitudeOptional,
    ValidateSchemaLongitudeRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class GeocoordBase(
    ValidateSchemaAddressRequired,
    ValidateSchemaLatitudeRequired,
    ValidateSchemaLongitudeRequired,
):
    address: str
    latitude: float
    longitude: float


class GeocoordCreate(GeocoordBase):
    pass


class GeocoordUpdate(
    ValidateSchemaAddressOptional,
    ValidateSchemaLatitudeOptional,
    ValidateSchemaLongitudeOptional,
):
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class GeocoordRead(GeocoordBase, BaseSchemaRead):
    id: UUID4
