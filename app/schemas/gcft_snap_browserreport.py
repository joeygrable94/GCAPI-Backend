from datetime import datetime
from typing import Optional

from pydantic import UUID4

from app.db.validators import (
    ValidateSchemaBrowserOptional,
    ValidateSchemaBrowserVersionOptional,
    ValidateSchemaCityOptional,
    ValidateSchemaCountryOptional,
    ValidateSchemaLanguageOptional,
    ValidateSchemaPlatformOptional,
    ValidateSchemaPlatformVersionOptional,
    ValidateSchemaStateOptional,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GcftSnapBrowserreportBase(
    ValidateSchemaBrowserOptional,
    ValidateSchemaBrowserVersionOptional,
    ValidateSchemaPlatformOptional,
    ValidateSchemaPlatformVersionOptional,
    ValidateSchemaCityOptional,
    ValidateSchemaCountryOptional,
    ValidateSchemaStateOptional,
    ValidateSchemaLanguageOptional,
):
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


class GcftSnapBrowserreportCreate(GcftSnapBrowserreportBase):
    pass


class GcftSnapBrowserreportUpdate(BaseSchema):
    pass


class GcftSnapBrowserreportRead(GcftSnapBrowserreportBase, BaseSchemaRead):
    id: UUID4
