from pydantic import UUID4

from app.db.acls.client_website import ClientWebsiteACL
from app.db.schemas.base import BaseSchema


class ClientWebsiteBase(BaseSchema):
    client_id: UUID4
    website_id: UUID4


class ClientWebsiteCreate(ClientWebsiteBase):
    pass


class ClientWebsiteUpdate(ClientWebsiteBase):
    pass


class ClientWebsiteRead(ClientWebsiteACL, ClientWebsiteBase):
    id: UUID4
