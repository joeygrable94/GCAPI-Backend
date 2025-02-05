from pydantic import UUID4

from app.core.schema import BaseSchema, BaseSchemaRead


class OrganizationPlatformBase(BaseSchema):
    organization_id: UUID4
    platform_id: UUID4


class OrganizationPlatformCreate(OrganizationPlatformBase):
    pass


class OrganizationPlatformUpdate(BaseSchema):
    organization_id: UUID4 | None = None
    platform_id: UUID4 | None = None


class OrganizationPlatformRead(OrganizationPlatformBase, BaseSchemaRead):
    id: UUID4
