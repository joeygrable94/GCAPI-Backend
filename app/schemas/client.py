from __future__ import annotations

from typing import Any, Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_description_optional,
    validate_slug_required,
    validate_title_optional,
    validate_title_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class ClientBase(BaseSchema):
    slug: str
    title: str
    description: Optional[str] = None
    is_active: bool = True

    _validate_slug = field_validator("slug", mode="before")(validate_slug_required)
    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )


class ClientCreate(ClientBase):
    title: str
    description: Optional[str] = None
    is_active: bool = True


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


class ClientDelete(BaseSchema):
    message: str
    user_id: UUID4
    client_id: UUID4
    task_id: UUID4 | str | Any | None = None
