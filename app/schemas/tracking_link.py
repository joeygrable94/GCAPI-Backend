from __future__ import annotations

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_destination_optional,
    validate_destination_required,
    validate_domain_optional,
    validate_domain_required,
    validate_scheme_optional,
    validate_scheme_required,
    validate_url_hash_optional,
    validate_url_hash_required,
    validate_url_optional,
    validate_url_path_optional,
    validate_url_path_required,
    validate_url_required,
    validate_utm_campaign_optional,
    validate_utm_content_optional,
    validate_utm_medium_optional,
    validate_utm_source_optional,
    validate_utm_term_optional,
)
from app.schemas.base import BaseSchema, BaseSchemaRead

# schemas


class TrackingLinkBaseParams(BaseSchema):
    scheme: str
    domain: str
    destination: str
    url_path: str = "/"
    utm_campaign: str | None = None
    utm_medium: str | None = None
    utm_source: str | None = None
    utm_content: str | None = None
    utm_term: str | None = None

    _validate_scheme = field_validator("scheme", mode="before")(
        validate_scheme_required
    )
    _validate_domain = field_validator("domain", mode="before")(
        validate_domain_required
    )
    _validate_destination = field_validator("destination", mode="before")(
        validate_destination_required
    )
    _validate_url_path = field_validator("url_path", mode="before")(
        validate_url_path_required
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


class TrackingLinkCreateRequest(BaseSchema):
    url: str
    is_active: bool | None = None
    client_id: UUID4 | None = None

    _validate_url = field_validator("url", mode="before")(validate_url_required)


class TrackingLinkCreate(BaseSchema):
    url: str
    url_hash: str
    scheme: str
    domain: str
    destination: str
    url_path: str
    utm_campaign: str | None = None
    utm_medium: str | None = None
    utm_source: str | None = None
    utm_content: str | None = None
    utm_term: str | None = None
    is_active: bool = True
    client_id: UUID4 | None = None

    _validate_url = field_validator("url", mode="before")(validate_url_required)
    _validate_url_hash = field_validator("url_hash", mode="before")(
        validate_url_hash_required
    )
    _validate_scheme = field_validator("scheme", mode="before")(
        validate_scheme_required
    )
    _validate_domain = field_validator("domain", mode="before")(
        validate_domain_required
    )
    _validate_destination = field_validator("destination", mode="before")(
        validate_destination_required
    )
    _validate_url_path = field_validator("url_path", mode="before")(
        validate_url_path_required
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
    client_id: UUID4 | None = None

    _validate_url = field_validator("url", mode="before")(validate_url_optional)


class TrackingLinkUpdate(BaseSchema):
    url: str | None = None
    url_hash: str | None = None
    scheme: str | None = None
    domain: str | None = None
    destination: str | None = None
    url_path: str | None = None
    utm_campaign: str | None = None
    utm_medium: str | None = None
    utm_source: str | None = None
    utm_content: str | None = None
    utm_term: str | None = None
    is_active: bool | None = None
    client_id: UUID4 | None = None

    _validate_url = field_validator("url", mode="before")(validate_url_optional)
    _validate_url_hash = field_validator("url_hash", mode="before")(
        validate_url_hash_optional
    )
    _validate_scheme = field_validator("scheme", mode="before")(
        validate_scheme_optional
    )
    _validate_domain = field_validator("domain", mode="before")(
        validate_domain_optional
    )
    _validate_destination = field_validator("destination", mode="before")(
        validate_destination_optional
    )
    _validate_url_path = field_validator("url_path", mode="before")(
        validate_url_path_optional
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
    scheme: str | None = None
    domain: str | None = None
    destination: str | None = None
    url_path: str
    utm_campaign: str | None = None
    utm_medium: str | None = None
    utm_source: str | None = None
    utm_content: str | None = None
    utm_term: str | None = None
    is_active: bool = True
    client_id: UUID4 | None = None

    _validate_url = field_validator("url", mode="before")(validate_url_required)
    _validate_url_hash = field_validator("url_hash", mode="before")(
        validate_url_hash_required
    )
    _validate_scheme = field_validator("scheme", mode="before")(
        validate_scheme_optional
    )
    _validate_domain = field_validator("domain", mode="before")(
        validate_domain_optional
    )
    _validate_destination = field_validator("destination", mode="before")(
        validate_destination_optional
    )
    _validate_url_path = field_validator("url_path", mode="before")(
        validate_url_path_required
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
