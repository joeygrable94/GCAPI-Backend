from datetime import datetime
from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_referrer_required,
    validate_utm_campaign_optional,
    validate_utm_content_optional,
    validate_utm_medium_optional,
    validate_utm_source_optional,
    validate_utm_term_optional,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GcftSnapTrafficsourceBase(BaseSchema):
    session_id: UUID4
    referrer: str
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_source: Optional[str] = None
    utm_term: Optional[str] = None
    visit_date: datetime
    gcft_id: UUID4
    snap_id: UUID4

    _validate_referrer = field_validator("referrer", mode="before")(
        validate_referrer_required
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


class GcftSnapTrafficsourceCreate(GcftSnapTrafficsourceBase):
    pass


class GcftSnapTrafficsourceUpdate(BaseSchema):
    pass


class GcftSnapTrafficsourceRead(GcftSnapTrafficsourceBase, BaseSchemaRead):
    id: UUID4
