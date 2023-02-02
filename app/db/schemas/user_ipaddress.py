from pydantic import UUID4

from app.db.schemas.base import BaseSchema


class UserIpBase(BaseSchema):
    user_id: UUID4
    ipaddress_id: UUID4


class UserIpCreate(UserIpBase):
    pass


class UserIpUpdate(UserIpBase):
    pass


class UserIpRead(UserIpBase):
    id: UUID4
