from pydantic import UUID4

from app.core.schema import BaseSchema, BaseSchemaRead


class UserOrganizationRoleBase(BaseSchema):
    user_id: UUID4
    organization_id: UUID4
    role_id: UUID4


class UserOrganizationRoleCreate(UserOrganizationRoleBase):
    pass


class UserOrganizationRoleUpdate(BaseSchema):
    user_id: UUID4 | None = None
    organization_id: UUID4 | None = None
    role_id: UUID4 | None = None


class UserOrganizationRoleRead(UserOrganizationRoleBase, BaseSchemaRead):
    id: UUID4
