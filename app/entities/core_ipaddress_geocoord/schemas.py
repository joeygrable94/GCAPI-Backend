from pydantic import UUID4

from app.core.schema import BaseSchema, BaseSchemaRead


class IpaddressGeocoordBase(BaseSchema):
    geocoord_id: UUID4
    ipaddress_id: UUID4


class IpaddressGeocoordCreate(IpaddressGeocoordBase):
    pass


class IpaddressGeocoordUpdate(BaseSchema):
    geocoord_id: UUID4 | None = None
    ipaddress_id: UUID4 | None = None


class IpaddressGeocoordRead(IpaddressGeocoordBase, BaseSchemaRead):
    id: UUID4
