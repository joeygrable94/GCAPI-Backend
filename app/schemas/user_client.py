from typing import Optional

from pydantic import UUID4

from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class UserClientBase(BaseSchema):
    user_id: UUID4
    client_id: UUID4


class UserClientCreate(UserClientBase):
    pass


class UserClientUpdate(BaseSchema):
    user_id: Optional[UUID4] = None
    client_id: Optional[UUID4] = None


class UserClientRead(UserClientBase, BaseSchemaRead):
    id: UUID4
