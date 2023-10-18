from typing import Optional

from pydantic import UUID4

from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class ClientWebsiteBase(BaseSchema):
    pass


class ClientWebsiteCreate(ClientWebsiteBase):
    client_id: UUID4
    website_id: UUID4


class ClientWebsiteUpdate(ClientWebsiteBase):
    client_id: Optional[UUID4] = None
    website_id: Optional[UUID4] = None


class ClientWebsiteRead(ClientWebsiteBase, BaseSchemaRead):
    id: UUID4
