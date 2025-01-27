from pydantic import UUID4

from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class UserClientBase(BaseSchema):
    user_id: UUID4
    client_id: UUID4


class UserClientCreate(UserClientBase):
    pass


class UserClientUpdate(BaseSchema):
    user_id: UUID4 | None = None
    client_id: UUID4 | None = None


class UserClientRead(UserClientBase, BaseSchemaRead):
    id: UUID4
