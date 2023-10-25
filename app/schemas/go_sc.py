from __future__ import annotations

from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import validate_title_optional, validate_title_required
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GoSearchConsolePropertyBase(BaseSchema):
    title: str
    client_id: UUID4
    website_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)


class GoSearchConsolePropertyCreate(GoSearchConsolePropertyBase):
    pass


class GoSearchConsolePropertyUpdate(BaseSchema):
    title: Optional[str] = None
    client_id: Optional[UUID4] = None
    website_id: Optional[UUID4] = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)


class GoSearchConsolePropertyRead(
    GoSearchConsolePropertyBase,
    BaseSchemaRead,
):
    id: UUID4
