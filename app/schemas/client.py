from __future__ import annotations

from typing import Any, Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_description_optional,
    validate_slug_required,
    validate_style_guide_optional,
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
    style_guide: Optional[str] = None

    _validate_slug = field_validator("slug", mode="before")(validate_slug_required)
    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )
    _validate_style_guide = field_validator("style_guide", mode="before")(
        validate_style_guide_optional
    )


class ClientCreate(ClientBase):
    title: str
    description: Optional[str] = None
    is_active: bool = True
    style_guide: Optional[str] = None


class ClientUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    style_guide: Optional[str] = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )
    _validate_style_guide = field_validator("style_guide", mode="before")(
        validate_style_guide_optional
    )


class ClientUpdateStyleGuide(BaseSchema):
    style_guide: Optional[str] = None

    _validate_style_guide = field_validator("style_guide", mode="before")(
        validate_style_guide_optional
    )


class ClientRead(ClientBase, BaseSchemaRead):
    id: UUID4


class ClientReadPublic(BaseSchema):
    id: UUID4
    title: str
    style_guide: Optional[str] = None

    _validate_style_guide = field_validator("style_guide", mode="before")(
        validate_style_guide_optional
    )


class ClientDelete(BaseSchema):
    message: str
    user_id: UUID4
    client_id: UUID4
    task_id: UUID4 | str | Any | None = None
