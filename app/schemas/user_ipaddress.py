from pydantic import UUID4

from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class UserIpaddressBase(BaseSchema):
    user_id: UUID4
    ipaddress_id: UUID4


class UserIpaddressCreate(UserIpaddressBase):
    pass


class UserIpaddressUpdate(BaseSchema):
    user_id: UUID4 | None = None
    ipaddress_id: UUID4 | None = None


class UserIpaddressRead(UserIpaddressBase, BaseSchemaRead):
    id: UUID4
