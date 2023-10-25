from datetime import datetime
from typing import Optional

from pydantic import UUID4, field_validator

from app.db.validators import (
    validate_browser_optional,
    validate_browser_version_optional,
    validate_city_optional,
    validate_country_optional,
    validate_language_optional,
    validate_platform_optional,
    validate_platform_version_optional,
    validate_state_optional,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GcftSnapBrowserreportBase(BaseSchema):
    session_id: UUID4
    browser: Optional[str] = None
    browser_version: Optional[str] = None
    platform: Optional[str] = None
    platform_version: Optional[str] = None
    desktop: Optional[bool] = None
    tablet: Optional[bool] = None
    mobile: Optional[bool] = None
    city: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    language: Optional[str] = None
    visit_date: datetime
    gcft_id: UUID4
    snap_id: UUID4

    _validate_browser = field_validator("browser", mode="before")(
        validate_browser_optional
    )
    _validate_browser_version = field_validator("browser_version", mode="before")(
        validate_browser_version_optional
    )
    _validate_platform = field_validator("platform", mode="before")(
        validate_platform_optional
    )
    _validate_platform_version = field_validator("platform_version", mode="before")(
        validate_platform_version_optional
    )
    _validate_city = field_validator("city", mode="before")(validate_city_optional)
    _validate_country = field_validator("country", mode="before")(
        validate_country_optional
    )
    _validate_state = field_validator("state", mode="before")(validate_state_optional)
    _validate_languda = field_validator("language", mode="before")(
        validate_language_optional
    )


class GcftSnapBrowserreportCreate(GcftSnapBrowserreportBase):
    pass


class GcftSnapBrowserreportUpdate(BaseSchema):
    pass


class GcftSnapBrowserreportRead(GcftSnapBrowserreportBase, BaseSchemaRead):
    id: UUID4
