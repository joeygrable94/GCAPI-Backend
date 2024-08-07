from pydantic import UUID4

from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class ClientTrackingLinkBase(BaseSchema):
    client_id: UUID4
    tracking_link_id: UUID4


class ClientTrackingLinkCreate(ClientTrackingLinkBase):
    pass


class ClientTrackingLinkUpdate(BaseSchema):
    client_id: UUID4 | None = None
    tracking_link_id: UUID4 | None = None


class ClientTrackingLinkRead(ClientTrackingLinkBase, BaseSchemaRead):
    id: UUID4
