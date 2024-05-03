from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_description_optional,
    validate_keys_optional,
    validate_title_optional,
    validate_title_required,
    validate_url_optional,
    validate_url_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class ClientReportBase(BaseSchema):
    title: str
    url: str
    description: Optional[str] = None
    keys: Optional[str] = None
    client_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_url = field_validator("url", mode="before")(validate_url_required)
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )
    _validate_keys = field_validator("keys", mode="before")(validate_keys_optional)


class ClientReportCreate(ClientReportBase):
    pass


class ClientReportUpdate(BaseSchema):
    title: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    keys: Optional[str] = None
    client_id: Optional[UUID4] = None
    created: Optional[datetime] = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)
    _validate_url = field_validator("url", mode="before")(validate_url_optional)
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )
    _validate_keys = field_validator("keys", mode="before")(validate_keys_optional)


class ClientReportRead(ClientReportBase, BaseSchemaRead):
    id: UUID4
