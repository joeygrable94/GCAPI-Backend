from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_bucket_name_optional,
    validate_bucket_name_required,
    validate_description_optional,
    validate_object_key_optional,
    validate_object_key_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class ClientBucketBase(BaseSchema):
    bucket_name: str
    object_key: str
    description: Optional[str] = None
    client_id: UUID4

    _validate_bucket_name = field_validator("bucket_name", mode="before")(
        validate_bucket_name_required
    )
    _validate_object_key = field_validator("object_key", mode="before")(
        validate_object_key_required
    )
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )


class ClientBucketCreate(ClientBucketBase):
    client_id: UUID4


class ClientBucketUpdate(BaseSchema):
    bucket_name: Optional[str] = None
    object_key: Optional[str] = None
    description: Optional[str] = None
    client_id: Optional[UUID4] = None

    _validate_bucket_name = field_validator("bucket_name", mode="before")(
        validate_bucket_name_optional
    )
    _validate_object_key = field_validator("object_key", mode="before")(
        validate_object_key_optional
    )
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )


class ClientBucketRead(ClientBucketBase, BaseSchemaRead):
    id: UUID4
