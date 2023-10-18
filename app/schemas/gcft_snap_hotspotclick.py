from datetime import datetime
from typing import Optional

from pydantic import UUID4

from app.db.validators import (
    ValidateSchemaBgColorOptional,
    ValidateSchemaHotspotContentOptional,
    ValidateSchemaHotspotIconNameOptional,
    ValidateSchemaHotspotNameOptional,
    ValidateSchemaHotspotTypeNameOptional,
    ValidateSchemaHotspotUserIconNameOptional,
    ValidateSchemaIconColorOptional,
    ValidateSchemaLinkedSnapNameOptional,
    ValidateSchemaReportingIdRequired,
    ValidateSchemaSnapFileNameOptional,
    ValidateSchemaTextColorOptional,
)
from app.schemas.base import BaseSchema, BaseSchemaRead


# schemas
class GcftSnapHotspotclickBase(
    ValidateSchemaReportingIdRequired,
    ValidateSchemaHotspotTypeNameOptional,
    ValidateSchemaHotspotContentOptional,
    ValidateSchemaHotspotIconNameOptional,
    ValidateSchemaHotspotNameOptional,
    ValidateSchemaHotspotUserIconNameOptional,
    ValidateSchemaLinkedSnapNameOptional,
    ValidateSchemaSnapFileNameOptional,
    ValidateSchemaIconColorOptional,
    ValidateSchemaBgColorOptional,
    ValidateSchemaTextColorOptional,
):
    session_id: UUID4
    reporting_id: str
    hotspot_type_name: Optional[str] = None
    hotspot_content: Optional[str] = None
    hotspot_icon_name: Optional[str] = None
    hotspot_name: Optional[str] = None
    hotspot_user_icon_name: Optional[str] = None
    linked_snap_name: Optional[str] = None
    snap_file_name: Optional[str] = None
    icon_color: Optional[str] = None
    bg_color: Optional[str] = None
    text_color: Optional[str] = None
    hotspot_update_date: datetime
    click_date: datetime
    gcft_id: UUID4
    snap_id: UUID4


class GcftSnapHotspotclickCreate(GcftSnapHotspotclickBase):
    pass


class GcftSnapHotspotclickUpdate(BaseSchema):
    pass


class GcftSnapHotspotclickRead(GcftSnapHotspotclickBase, BaseSchemaRead):
    id: UUID4
