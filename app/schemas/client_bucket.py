from typing import Optional

from pydantic import UUID4

from app.db.acls import ClientBucketACL
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
    description: Optional[str]
    client_id: UUID4


class ClientBucketCreate(ClientBucketBase):
    client_id: UUID4


class ClientBucketUpdate(
    ValidateSchemaBucketNameOptional,
    ValidateSchemaObjectKeyOptional,
    ValidateSchemaDescriptionOptional,
):
    bucket_name: Optional[str]
    object_key: Optional[str]
    description: Optional[str]
    client_id: Optional[UUID4]


class ClientBucketRead(ClientBucketACL, ClientBucketBase, BaseSchemaRead):
    id: UUID4
