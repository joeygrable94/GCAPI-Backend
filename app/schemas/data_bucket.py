from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_bucket_name_required,
    validate_bucket_prefix_required,
    validate_description_optional,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class DataBucketBase(BaseSchema):
    bucket_name: str
    bucket_prefix: str
    description: Optional[str] = None
    client_id: UUID4
    bdx_feed_id: UUID4 | None = None
    gcft_id: UUID4 | None = None

    _validate_bucket_name = field_validator("bucket_name", mode="before")(
        validate_bucket_name_required
    )
    _validate_bucket_prefix = field_validator("bucket_prefix", mode="before")(
        validate_bucket_prefix_required
    )
    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )


class DataBucketCreate(DataBucketBase):
    pass


class DataBucketUpdate(BaseSchema):
    description: Optional[str] = None

    _validate_description = field_validator("description", mode="before")(
        validate_description_optional
    )


class DataBucketRead(DataBucketBase, BaseSchemaRead):
    id: UUID4
