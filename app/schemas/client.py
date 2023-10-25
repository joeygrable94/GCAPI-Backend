from __future__ import annotations

from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_description_optional,
    validate_title_optional,
    validate_title_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class ClientBase(BaseSchema):
    title: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )


class ClientCreate(ClientBase):
    title: str
    description: Optional[str] = None


class ClientUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )


class ClientRead(ClientBase, BaseSchemaRead):
    id: UUID4
