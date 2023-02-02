from typing import List, Optional

from pydantic import UUID4, validator

from app.db.acls.ipaddress import IpAddressACL
from app.db.schemas.base import BaseSchema


# validators
class ValidateIpAddressRequired(BaseSchema):
    address: str

    @validator("address")
    def limits_address(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("ip addresses must contain 3 or more characters")
        if len(v) > 64:
            raise ValueError("ip addresses must contain less than 64 characters")
        return v


class ValidateIpAddressOptional(BaseSchema):
    address: Optional[str]

    @validator("address")
    def limits_address(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) < 3:
            raise ValueError("ip addresses must contain 3 or more characters")
        if v and len(v) > 64:
            raise ValueError("ip addresses must contain less than 64 characters")
        return v


class ValidateIpIspOptional(BaseSchema):
    isp: Optional[str]

    @validator("isp")
    def limits_isp(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) > 255:
            raise ValueError(
                "ip internet service providers must contain less than 255 characters"
            )
        return v


class ValidateIpLocationOptional(BaseSchema):
    location: Optional[str]

    @validator("location")
    def limits_location(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) > 500:
            raise ValueError("ip location must contain less than 500 characters")
        return v


class IpAddressBase(BaseSchema):
    isp: Optional[str] = None
    location: Optional[str] = None
    geocoord_id: Optional[UUID4] = None


class IpAddressCreate(
    ValidateIpAddressRequired,
    ValidateIpIspOptional,
    ValidateIpLocationOptional,
    IpAddressBase,
):
    address: str


class IpAddressUpdate(
    ValidateIpAddressOptional,
    ValidateIpIspOptional,
    ValidateIpLocationOptional,
    IpAddressBase,
):
    address: Optional[str]


class IpAddressRead(
    IpAddressACL,
    ValidateIpAddressRequired,
    ValidateIpIspOptional,
    ValidateIpLocationOptional,
    IpAddressBase,
):
    id: UUID4


# relationships
class IpAddressReadRelations(IpAddressRead):
    users: Optional[List["UserRead"]] = []


# import and update pydantic relationship refs
from app.db.schemas.user import UserRead  # noqa: E402

IpAddressReadRelations.update_forward_refs()
