from datetime import datetime
from typing import Optional

from pydantic import UUID4

from app.db.acls import GcftSnapBrowserreportACL
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
    browser: Optional[str]
    browser_version: Optional[str]
    platform: Optional[str]
    platform_version: Optional[str]
    desktop: Optional[bool]
    tablet: Optional[bool]
    mobile: Optional[bool]
    city: Optional[str]
    country: Optional[str]
    state: Optional[str]
    language: Optional[str]
    visit_date: datetime
    gcft_id: UUID4
    snap_id: UUID4


class GcftSnapBrowserreportCreate(GcftSnapBrowserreportBase):
    pass


class GcftSnapBrowserreportUpdate(BaseSchema):
    pass


class GcftSnapBrowserreportRead(
    GcftSnapBrowserreportACL, GcftSnapBrowserreportBase, BaseSchemaRead
):
    id: UUID4
