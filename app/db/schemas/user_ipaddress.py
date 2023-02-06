from typing import Optional

from pydantic import UUID4

from app.db.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class UserIpBase(BaseSchema):
    pass


class UserIpCreate(UserIpBase):
    user_id: UUID4
    ipaddress_id: UUID4


class UserIpUpdate(UserIpBase):
    user_id: Optional[UUID4]
    ipaddress_id: Optional[UUID4]


class UserIpRead(UserIpBase, BaseSchemaRead):
    id: UUID4
