from pydantic import UUID4

from app.db.schemas.base import BaseSchema


class UserClientBase(BaseSchema):
    user_id: UUID4
    client_id: UUID4


class UserClientCreate(UserClientBase):
    pass


class UserClientUpdate(UserClientBase):
    pass


class UserClientRead(UserClientBase):
    id: UUID4
