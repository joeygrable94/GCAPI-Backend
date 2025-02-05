from pydantic import UUID4

from app.core.schema import BaseSchema, BaseSchemaRead


class OrganizationWebsiteBase(BaseSchema):
    organization_id: UUID4
    website_id: UUID4


class OrganizationWebsiteCreate(OrganizationWebsiteBase):
    pass


class OrganizationWebsiteUpdate(BaseSchema):
    organization_id: UUID4 | None = None
    website_id: UUID4 | None = None


class OrganizationWebsiteRead(OrganizationWebsiteBase, BaseSchemaRead):
    id: UUID4
