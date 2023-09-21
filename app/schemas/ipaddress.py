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
    geocoord_id: Optional[UUID4] = None


class IpaddressCreate(IpaddressBase):
    pass


class IpaddressUpdate(
    ValidateSchemaIpOptional,
    ValidateSchemaIspOptional,
    ValidateSchemaIpLocationOptional,
):
    ip: Optional[str] = None
    isp: Optional[str] = None
    location: Optional[str] = None
    geocoord_id: Optional[UUID4] = None


class IpaddressRead(IpaddressACL, IpaddressBase, BaseSchemaRead):
    id: UUID4
