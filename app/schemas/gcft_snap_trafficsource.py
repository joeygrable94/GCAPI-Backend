from datetime import datetime
from typing import Optional

from pydantic import UUID4

from app.db.acls import GcftSnapTrafficsourceACL
from app.db.validators import (
    ValidateSchemaReferrerRequired,
    ValidateSchemaUtmCampaignOptional,
    ValidateSchemaUtmContentOptional,
    ValidateSchemaUtmMediumOptional,
    ValidateSchemaUtmSourceOptional,
    ValidateSchemaUtmTermOptional,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GcftSnapTrafficsourceBase(
    ValidateSchemaReferrerRequired,
    ValidateSchemaUtmCampaignOptional,
    ValidateSchemaUtmContentOptional,
    ValidateSchemaUtmMediumOptional,
    ValidateSchemaUtmSourceOptional,
    ValidateSchemaUtmTermOptional,
):
    session_id: UUID4
    referrer: str
    utm_campaign: Optional[str]
    utm_content: Optional[str]
    utm_medium: Optional[str]
    utm_source: Optional[str]
    utm_term: Optional[str]
    visit_date: datetime
    gcft_id: UUID4
    snap_id: UUID4


class GcftSnapTrafficsourceCreate(GcftSnapTrafficsourceBase):
    pass


class GcftSnapTrafficsourceUpdate(BaseSchema):
    pass


class GcftSnapTrafficsourceRead(
    GcftSnapTrafficsourceACL, GcftSnapTrafficsourceBase, BaseSchemaRead
):
    id: UUID4
