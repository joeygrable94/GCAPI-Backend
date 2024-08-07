from __future__ import annotations

from pydantic import field_validator

from app.db.validators import (
    validate_url_hash_optional,
    validate_url_hash_required,
    validate_url_optional,
    validate_url_required,
    validate_utm_campaign_optional,
    validate_utm_content_optional,
    validate_utm_medium_optional,
    validate_utm_source_optional,
    validate_utm_term_optional,
)
from app.schemas.base import BaseSchema, BaseSchemaRead

# schemas


class TrackingLinkBaseUtmParams(BaseSchema):
    utm_campaign: str | None = None
    utm_medium: str | None = None
    utm_source: str | None = None
    utm_content: str | None = None
    utm_term: str | None = None

    _validate_utm_campaign = field_validator("utm_campaign", mode="before")(
        validate_utm_campaign_optional
    )
    _validate_utm_content = field_validator("utm_content", mode="before")(
        validate_utm_content_optional
    )
    _validate_utm_medium = field_validator("utm_medium", mode="before")(
        validate_utm_medium_optional
    )
    _validate_utm_source = field_validator("utm_source", mode="before")(
        validate_utm_source_optional
    )
    _validate_utm_term = field_validator("utm_term", mode="before")(
        validate_utm_term_optional
    )


class TrackingLinkCreateRequest(BaseSchema):
    url: str
    is_active: bool = True

    _validate_url = field_validator("url", mode="before")(validate_url_required)


class TrackingLinkCreate(BaseSchema):
    url: str
    url_hash: str
    utm_campaign: str | None = None
    utm_medium: str | None = None
    utm_source: str | None = None
    utm_content: str | None = None
    utm_term: str | None = None
    is_active: bool = True

    _validate_url = field_validator("url", mode="before")(validate_url_required)
    _validate_url_hash = field_validator("url_hash", mode="before")(
        validate_url_hash_required
    )
    _validate_utm_campaign = field_validator("utm_campaign", mode="before")(
        validate_utm_campaign_optional
    )
    _validate_utm_content = field_validator("utm_content", mode="before")(
        validate_utm_content_optional
    )
    _validate_utm_medium = field_validator("utm_medium", mode="before")(
        validate_utm_medium_optional
    )
    _validate_utm_source = field_validator("utm_source", mode="before")(
        validate_utm_source_optional
    )
    _validate_utm_term = field_validator("utm_term", mode="before")(
        validate_utm_term_optional
    )


class TrackingLinkUpdateRequest(BaseSchema):
    url: str | None = None
    is_active: bool | None = None

    _validate_url = field_validator("url", mode="before")(validate_url_optional)


class TrackingLinkUpdate(BaseSchema):
    url: str | None = None
    url_hash: str | None = None
    utm_campaign: str | None = None
    utm_medium: str | None = None
    utm_source: str | None = None
    utm_content: str | None = None
    utm_term: str | None = None
    is_active: bool | None = None

    _validate_url = field_validator("url", mode="before")(validate_url_optional)
    _validate_url_hash = field_validator("url_hash", mode="before")(
        validate_url_hash_optional
    )
    _validate_utm_campaign = field_validator("utm_campaign", mode="before")(
        validate_utm_campaign_optional
    )
    _validate_utm_content = field_validator("utm_content", mode="before")(
        validate_utm_content_optional
    )
    _validate_utm_medium = field_validator("utm_medium", mode="before")(
        validate_utm_medium_optional
    )
    _validate_utm_source = field_validator("utm_source", mode="before")(
        validate_utm_source_optional
    )
    _validate_utm_term = field_validator("utm_term", mode="before")(
        validate_utm_term_optional
    )


class TrackingLinkRead(BaseSchemaRead):
    url: str
    url_hash: str
    utm_campaign: str | None = None
    utm_medium: str | None = None
    utm_source: str | None = None
    utm_content: str | None = None
    utm_term: str | None = None
    is_active: bool = True

    _validate_url = field_validator("url", mode="before")(validate_url_required)
    _validate_url_hash = field_validator("url_hash", mode="before")(
        validate_url_hash_required
    )
    _validate_utm_campaign = field_validator("utm_campaign", mode="before")(
        validate_utm_campaign_optional
    )
    _validate_utm_content = field_validator("utm_content", mode="before")(
        validate_utm_content_optional
    )
    _validate_utm_medium = field_validator("utm_medium", mode="before")(
        validate_utm_medium_optional
    )
    _validate_utm_source = field_validator("utm_source", mode="before")(
        validate_utm_source_optional
    )
    _validate_utm_term = field_validator("utm_term", mode="before")(
        validate_utm_term_optional
    )
