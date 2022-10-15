from pydantic import UUID4

from app.db.schemas.base import BaseSchema, BaseSchemaRead


class AccessTokenInDB(BaseSchema):
    token: str
    user_id: UUID4
    is_revoked: bool


class AccessTokenCreate(BaseSchema):
    token: str
    user_id: UUID4
    is_revoked: bool = False


class AccessTokenUpdate(BaseSchema):
    is_revoked: bool = False


class AccessTokenRead(BaseSchemaRead):
    token: str
    user_id: UUID4
    is_revoked: bool
