from typing import Optional

from pydantic import UUID4

from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class UserIpaddressBase(BaseSchema):
    pass


class UserIpaddressCreate(UserIpaddressBase):
    user_id: UUID4
    ipaddress_id: UUID4


class UserIpaddressUpdate(UserIpaddressBase):
    user_id: Optional[UUID4] = None
    ipaddress_id: Optional[UUID4] = None


class UserIpaddressRead(UserIpaddressBase, BaseSchemaRead):
    id: UUID4
