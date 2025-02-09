from pydantic import UUID4

from app.core.schema import BaseSchema, BaseSchemaRead


class UserOrganizationBase(BaseSchema):
    user_id: UUID4
    organization_id: UUID4


class UserOrganizationCreate(UserOrganizationBase):
    pass


class UserOrganizationUpdate(BaseSchema):
    user_id: UUID4 | None = None
    organization_id: UUID4 | None = None


class UserOrganizationRead(UserOrganizationBase, BaseSchemaRead):
    id: UUID4
