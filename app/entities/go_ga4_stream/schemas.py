from pydantic import UUID4, field_validator

from app.core.schema import BaseSchema, BaseSchemaRead
from app.db.validators import (
    validate_measurement_id_required,
    validate_stream_id_required,
    validate_title_optional,
    validate_title_required,
)


class GoAnalytics4StreamBase(BaseSchema):
    title: str
    stream_id: str
    measurement_id: str
    ga4_id: UUID4
    website_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_stream_id = field_validator("stream_id", mode="before")(
        validate_stream_id_required
    )
    _validate_measurement_id = field_validator("measurement_id", mode="before")(
        validate_measurement_id_required
    )


class GoAnalytics4StreamCreate(GoAnalytics4StreamBase):
    pass


class RequestGoAnalytics4StreamCreate(BaseSchema):
    title: str
    stream_id: str
    measurement_id: str
    ga4_id: UUID4
    website_id: UUID4
    client_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_required)
    _validate_stream_id = field_validator("stream_id", mode="before")(
        validate_stream_id_required
    )
    _validate_measurement_id = field_validator("measurement_id", mode="before")(
        validate_measurement_id_required
    )


class GoAnalytics4StreamUpdate(BaseSchema):
    title: str | None = None
    website_id: UUID4

    _validate_title = field_validator("title", mode="before")(validate_title_optional)


class GoAnalytics4StreamRead(GoAnalytics4StreamBase, BaseSchemaRead):
    id: UUID4
