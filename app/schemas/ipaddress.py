from typing import Optional

from pydantic import UUID4

from app.db.acls import IpaddressACL
from app.db.validators import (
    ValidateSchemaIpLocationOptional,
    ValidateSchemaIpLocationRequired,
    ValidateSchemaIpOptional,
    ValidateSchemaIpRequired,
    ValidateSchemaIspOptional,
    ValidateSchemaIspRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class IpaddressBase(
    ValidateSchemaIpRequired,
    ValidateSchemaIspRequired,
    ValidateSchemaIpLocationRequired,
):
    ip: str
    isp: str
    location: str
    geocoord_id: Optional[UUID4]


class IpaddressCreate(IpaddressBase):
    pass


class IpaddressUpdate(
    ValidateSchemaIpOptional,
    ValidateSchemaIspOptional,
    ValidateSchemaIpLocationOptional,
):
    ip: Optional[str]
    isp: Optional[str]
    location: Optional[str]
    geocoord_id: Optional[UUID4]


class IpaddressRead(IpaddressACL, IpaddressBase, BaseSchemaRead):
    id: UUID4
