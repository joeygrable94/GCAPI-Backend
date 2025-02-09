from pydantic import UUID4

from app.core.schema import BaseSchema, BaseSchemaRead


class UserPermissionBase(BaseSchema):
    user_id: UUID4
    permission_id: UUID4


class UserPermissionCreate(UserPermissionBase):
    pass


class UserPermissionUpdate(BaseSchema):
    user_id: UUID4 | None = None
    permission_id: UUID4 | None = None


class UserPermissionRead(UserPermissionBase, BaseSchemaRead):
    id: UUID4
