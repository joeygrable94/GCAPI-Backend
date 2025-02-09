from pydantic import UUID4

from app.core.schema import BaseSchema, BaseSchemaRead


class RolePermissionBase(BaseSchema):
    role_id: UUID4
    permission_id: UUID4


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionUpdate(BaseSchema):
    role_id: UUID4 | None = None
    permission_id: UUID4 | None = None


class RolePermissionRead(RolePermissionBase, BaseSchemaRead):
    id: UUID4
