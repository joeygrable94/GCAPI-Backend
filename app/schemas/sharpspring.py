from __future__ import annotations

from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_api_key_optional,
    validate_api_key_required,
    validate_secret_key_optional,
    validate_secret_key_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class SharpspringBase(BaseSchema):
    api_key: str
    secret_key: str
    client_id: UUID4

    _validate_api_key = field_validator("api_key", mode="before")(
        validate_api_key_required
    )
    _validate_secret_key = field_validator("secret_key", mode="before")(
        validate_secret_key_required
    )


class SharpspringCreate(SharpspringBase):
    pass


class SharpspringUpdate(BaseSchema):
    api_key: Optional[str] = None
    secret_key: Optional[str] = None
    client_id: Optional[UUID4] = None

    _validate_api_key = field_validator("api_key", mode="before")(
        validate_api_key_optional
    )
    _validate_secret_key = field_validator("secret_key", mode="before")(
        validate_secret_key_optional
    )


class SharpspringRead(SharpspringBase, BaseSchemaRead):
    id: UUID4
