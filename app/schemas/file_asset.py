from __future__ import annotations

from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_caption_optional,
    validate_file_name_optional,
    validate_file_name_required,
    validate_mime_type_optional,
    validate_mime_type_required,
    validate_size_kb_optional,
    validate_title_optional,
    validate_title_required,
)
from app.schemas.base import BaseSchemaRead


# schemas
class FileAssetBase(BaseSchemaRead):
    file_name: str
    mime_type: str
    size_kb: int | None = None
    title: str
    caption: Optional[str] = None
    user_id: UUID4
    client_id: UUID4
    geocoord_id: Optional[UUID4] = None
    bdx_feed_id: Optional[UUID4] = None

    _validate_file_name = field_validator("file_name", mode="before")(
        validate_file_name_required
    )
    _validate_mime_type = field_validator("mime_type", mode="before")(
        validate_mime_type_required
    )
    _validate_size_kb = field_validator("size_kb", mode="before")(
        validate_size_kb_optional
    )
    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_caption = field_validator("caption", mode="before")(
        validate_caption_optional
    )


class FileAssetCreate(FileAssetBase):
    pass


class FileAssetUpdate(BaseSchemaRead):
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    size_kb: Optional[int] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    client_id: Optional[UUID4] = None
    geocoord_id: Optional[UUID4] = None
    bdx_feed_id: Optional[UUID4] = None

    _validate_file_name = field_validator("file_name", mode="before")(
        validate_file_name_optional
    )
    _validate_mime_type = field_validator("mime_type", mode="before")(
        validate_mime_type_optional
    )
    _validate_size_kb = field_validator("size_kb", mode="before")(
        validate_size_kb_optional
    )
    _validate_title = field_validator("title", mode="before")(validate_title_optional)
    _validate_caption = field_validator("caption", mode="before")(
        validate_caption_optional
    )


class FileAssetRead(FileAssetBase, BaseSchemaRead):
    id: UUID4
