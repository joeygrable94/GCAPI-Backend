from __future__ import annotations

from typing import Optional

from pydantic import UUID4

from app.db.acls import FileAssetACL
from app.db.validators import (
    ValidateSchemaCaptionOptional,
    ValidateSchemaExtensionOptional,
    ValidateSchemaExtensionRequired,
    ValidateSchemaKeysOptional,
    ValidateSchemaNameOptional,
    ValidateSchemaNameRequired,
    ValidateSchemaSizeKbOptional,
    ValidateSchemaSizeKbRequired,
    ValidateSchemaTitleOptional,
    ValidateSchemaTitleRequired,
    ValidFileExtensionEnum,
)
from app.schemas.base import BaseSchemaRead


# schemas
class FileAssetBase(
    ValidateSchemaNameRequired,
    ValidateSchemaExtensionRequired,
    ValidateSchemaSizeKbRequired,
    ValidateSchemaTitleRequired,
    ValidateSchemaCaptionOptional,
    ValidateSchemaKeysOptional,
    BaseSchemaRead,
):
    name: str
    extension: ValidFileExtensionEnum
    size_kb: int
    title: str
    caption: Optional[str]
    keys: Optional[str]
    is_private: bool
    user_id: UUID4
    bucket_id: UUID4
    client_id: UUID4
    geocoord_id: Optional[UUID4] = None
    bdx_feed_id: Optional[UUID4] = None


class FileAssetCreate(FileAssetBase):
    pass


class FileAssetUpdate(
    ValidateSchemaNameOptional,
    ValidateSchemaExtensionOptional,
    ValidateSchemaSizeKbOptional,
    ValidateSchemaTitleOptional,
    ValidateSchemaCaptionOptional,
    ValidateSchemaKeysOptional,
    BaseSchemaRead,
):
    name: Optional[str]
    extension: Optional[ValidFileExtensionEnum]
    size_kb: Optional[int]
    title: Optional[str]
    caption: Optional[str]
    keys: Optional[str]
    is_private: Optional[bool]
    user_id: Optional[UUID4]
    bucket_id: Optional[UUID4]
    client_id: Optional[UUID4]
    geocoord_id: Optional[UUID4] = None
    bdx_feed_id: Optional[UUID4] = None


class FileAssetRead(FileAssetACL, FileAssetBase, BaseSchemaRead):
    id: UUID4


# relationships
class FileAssetReadRelations(FileAssetRead):
    geotag: Optional["GeocoordRead"] = None


from app.schemas.geocoord import GeocoordRead  # noqa: E402

FileAssetReadRelations.update_forward_refs()
