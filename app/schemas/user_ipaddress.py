from typing import Optional

from pydantic import UUID4

from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class UserIpaddressBase(BaseSchema):
    user_id: UUID4
    ipaddress_id: UUID4


class UserIpaddressCreate(UserIpaddressBase):
    pass


class UserIpaddressUpdate(BaseSchema):
    user_id: Optional[UUID4] = None
    ipaddress_id: Optional[UUID4] = None


class UserIpaddressRead(UserIpaddressBase, BaseSchemaRead):
    id: UUID4
