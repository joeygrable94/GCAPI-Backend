from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_stream_id_required,
    validate_title_optional,
    validate_title_required,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GoAnalytics4StreamBase(BaseSchema):
    title: str
    stream_id: str
    ga4_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_stream_id = field_validator("stream_id", mode="before")(
        validate_stream_id_required
    )


class GoAnalytics4StreamCreate(GoAnalytics4StreamBase):
    pass


class GoAnalytics4StreamUpdate(BaseSchema):
    title: Optional[str] = None

    _validate_title = field_validator("title", mode="before")(validate_title_optional)


class GoAnalytics4StreamRead(
    GoAnalytics4StreamBase,
    BaseSchemaRead,
):
    id: UUID4
