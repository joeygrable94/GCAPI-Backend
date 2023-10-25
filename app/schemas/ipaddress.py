from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_ip_location_optional,
    validate_ip_location_required,
    validate_ip_optional,
    validate_ip_required,
    validate_isp_optional,
    validate_isp_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class IpaddressBase(BaseSchema):
    address: str
    isp: str
    location: str
    geocoord_id: Optional[UUID4] = None

    _validate_address = field_validator("address", mode="before")(validate_ip_required)
    _validate_isp = field_validator("isp", mode="before")(validate_isp_required)
    _validate_location = field_validator("location", mode="before")(
        validate_ip_location_required
    )


class IpaddressCreate(IpaddressBase):
    pass


class IpaddressUpdate(BaseSchema):
    address: Optional[str] = None
    isp: Optional[str] = None
    location: Optional[str] = None
    geocoord_id: Optional[UUID4] = None

    _validate_address = field_validator("address", mode="before")(validate_ip_optional)
    _validate_isp = field_validator("isp", mode="before")(validate_isp_optional)
    _validate_location = field_validator("location", mode="before")(
        validate_ip_location_optional
    )


class IpaddressRead(IpaddressBase, BaseSchemaRead):
    id: UUID4
