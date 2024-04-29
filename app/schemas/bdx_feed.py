from __future__ import annotations

from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_password_optional,
    validate_password_required,
    validate_serverhost_optional,
    validate_serverhost_required,
    validate_username_optional,
    validate_username_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class BdxFeedBase(BaseSchema):
    username: str
    password: str
    serverhost: str
    client_id: UUID4

    _validate_username = field_validator("username", mode="before")(
        validate_username_required
    )
    _validate_password = field_validator("password", mode="before")(
        validate_password_required
    )
    _validate_serverhost = field_validator("serverhost", mode="before")(
        validate_serverhost_required
    )


class BdxFeedCreate(BdxFeedBase):
    pass


class BdxFeedUpdate(BaseSchema):
    username: Optional[str] = None
    password: Optional[str] = None
    serverhost: Optional[str] = None
    client_id: Optional[UUID4] = None

    _validate_username = field_validator("username", mode="before")(
        validate_username_optional
    )
    _validate_password = field_validator("password", mode="before")(
        validate_password_optional
    )
    _validate_serverhost = field_validator("serverhost", mode="before")(
        validate_serverhost_optional
    )


class BdxFeedRead(BdxFeedBase, BaseSchemaRead):
    id: UUID4
