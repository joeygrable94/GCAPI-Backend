from pydantic import UUID4

from app.db.acls.user_client import UserClientACL
from app.db.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class UserClientBase(BaseSchema):
    user_id: UUID4
    client_id: UUID4


class UserClientCreate(UserClientBase):
    pass


class UserClientUpdate(UserClientBase):
    pass


class UserClientRead(UserClientACL, UserClientBase, BaseSchemaRead):
    id: UUID4
