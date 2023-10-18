from typing import Optional

from pydantic import UUID4

from app.db.validators import (
    ValidateSchemaBucketNameOptional,
    ValidateSchemaBucketNameRequired,
    ValidateSchemaDescriptionOptional,
    ValidateSchemaObjectKeyOptional,
    ValidateSchemaObjectKeyRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class ClientBucketBase(
    ValidateSchemaBucketNameRequired,
    ValidateSchemaObjectKeyRequired,
    ValidateSchemaDescriptionOptional,
):
    bucket_name: str
    object_key: str
    description: Optional[str] = None
    client_id: UUID4


class ClientBucketCreate(ClientBucketBase):
    client_id: UUID4


class ClientBucketUpdate(
    ValidateSchemaBucketNameOptional,
    ValidateSchemaObjectKeyOptional,
    ValidateSchemaDescriptionOptional,
):
    bucket_name: Optional[str] = None
    object_key: Optional[str] = None
    description: Optional[str] = None
    client_id: Optional[UUID4] = None


class ClientBucketRead(ClientBucketBase, BaseSchemaRead):
    id: UUID4
