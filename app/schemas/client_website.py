from pydantic import UUID4

from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class ClientWebsiteBase(BaseSchema):
    client_id: UUID4
    website_id: UUID4


class ClientWebsiteCreate(ClientWebsiteBase):
    pass


class ClientWebsiteUpdate(BaseSchema):
    client_id: UUID4 | None = None
    website_id: UUID4 | None = None


class ClientWebsiteRead(ClientWebsiteBase, BaseSchemaRead):
    id: UUID4
