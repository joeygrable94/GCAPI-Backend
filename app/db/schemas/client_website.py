from typing import Optional

from pydantic import UUID4

from app.db.acls.client_website import ClientWebsiteACL
from app.db.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class ClientWebsiteBase(BaseSchema):
    pass


class ClientWebsiteCreate(ClientWebsiteBase):
    client_id: UUID4
    website_id: UUID4


class ClientWebsiteUpdate(ClientWebsiteBase):
    client_id: Optional[UUID4]
    website_id: Optional[UUID4]


class ClientWebsiteRead(ClientWebsiteACL, ClientWebsiteBase, BaseSchemaRead):
    id: UUID4
