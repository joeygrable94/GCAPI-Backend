from typing import Optional

from pydantic import UUID4

from app.db.acls import UserClientACL
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class UserClientBase(BaseSchema):
    pass


class UserClientCreate(UserClientBase):
    user_id: UUID4
    client_id: UUID4


class UserClientUpdate(UserClientBase):
    user_id: Optional[UUID4] = None
    client_id: Optional[UUID4] = None


class UserClientRead(UserClientACL, UserClientBase, BaseSchemaRead):
    id: UUID4
