from typing import Optional

from pydantic import UUID4

from app.db.acls import GeocoordACL
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
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]


class GeocoordRead(GeocoordACL, GeocoordBase, BaseSchemaRead):
    id: UUID4
