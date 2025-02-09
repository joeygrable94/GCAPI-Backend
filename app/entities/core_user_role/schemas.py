from pydantic import UUID4

from app.core.schema import BaseSchema, BaseSchemaRead


class UserRoleBase(BaseSchema):
    user_id: UUID4
    role_id: UUID4


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(BaseSchema):
    user_id: UUID4 | None = None
    role_id: UUID4 | None = None


class UserRoleRead(UserRoleBase, BaseSchemaRead):
    id: UUID4
