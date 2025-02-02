from pydantic import UUID4

from app.core.schema import BaseSchema, BaseSchemaRead


class ClientPlatformBase(BaseSchema):
    client_id: UUID4
    platform_id: UUID4


class ClientPlatformCreate(ClientPlatformBase):
    pass


class ClientPlatformUpdate(BaseSchema):
    client_id: UUID4 | None = None
    platform_id: UUID4 | None = None


class ClientPlatformRead(ClientPlatformBase, BaseSchemaRead):
    id: UUID4
