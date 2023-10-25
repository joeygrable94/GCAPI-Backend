from __future__ import annotations

from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    ValidFileExtensionEnum,
    validate_caption_optional,
    validate_filename_optional,
    validate_filename_required,
    validate_keys_optional,
    validate_size_kb_optional,
    validate_size_kb_required,
    validate_title_optional,
    validate_title_required,
)
from app.schemas.base import BaseSchemaRead


# schemas
class FileAssetBase(BaseSchemaRead):
    filename: str
    extension: ValidFileExtensionEnum
    size_kb: int
    title: str
    caption: Optional[str] = None
    keys: Optional[str] = None
    is_private: bool
    user_id: UUID4
    bucket_id: UUID4
    client_id: UUID4
    geocoord_id: Optional[UUID4] = None
    bdx_feed_id: Optional[UUID4] = None

    _validate_filename = field_validator("filename", mode="before")(
        validate_filename_required
    )
    _validate_size_kb = field_validator("size_kb", mode="before")(
        validate_size_kb_required
    )
    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_caption = field_validator("caption", mode="before")(
        validate_caption_optional
    )
    _validate_keys = field_validator("keys", mode="before")(validate_keys_optional)


class FileAssetCreate(FileAssetBase):
    pass


class FileAssetUpdate(BaseSchemaRead):
    filename: Optional[str] = None
    extension: Optional[ValidFileExtensionEnum] = None
    size_kb: Optional[int] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    keys: Optional[str] = None
    is_private: Optional[bool] = None
    user_id: Optional[UUID4] = None
    bucket_id: Optional[UUID4] = None
    client_id: Optional[UUID4] = None
    geocoord_id: Optional[UUID4] = None
    bdx_feed_id: Optional[UUID4] = None

    _validate_filename = field_validator("filename", mode="before")(
        validate_filename_optional
    )
    _validate_size_kb = field_validator("size_kb", mode="before")(
        validate_size_kb_optional
    )
    _validate_title = field_validator("title", mode="before")(validate_title_optional)
    _validate_caption = field_validator("caption", mode="before")(
        validate_caption_optional
    )
    _validate_keys = field_validator("keys", mode="before")(validate_keys_optional)


class FileAssetRead(FileAssetBase, BaseSchemaRead):
    id: UUID4
