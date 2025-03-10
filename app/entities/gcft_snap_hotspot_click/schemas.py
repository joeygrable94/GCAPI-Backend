from datetime import datetime

from pydantic import UUID4, field_validator

from app.core.schema import BaseSchema, BaseSchemaRead
from app.db.validators import (
    validate_bg_color_optional,
    validate_hotspot_content_optional,
    validate_hotspot_icon_name_optional,
    validate_hotspot_name_optional,
    validate_hotspot_type_name_optional,
    validate_hotspot_user_icon_name_optional,
    validate_icon_color_optional,
    validate_linked_snap_name_optional,
    validate_reporting_id_required,
    validate_snap_file_name_optional,
    validate_text_color_optional,
)


class GcftSnapHotspotclickBase(BaseSchema):
    session_id: UUID4
    reporting_id: str
    hotspot_type_name: str | None = None
    hotspot_content: str | None = None
    hotspot_icon_name: str | None = None
    hotspot_name: str | None = None
    hotspot_user_icon_name: str | None = None
    linked_snap_name: str | None = None
    snap_file_name: str | None = None
    icon_color: str | None = None
    bg_color: str | None = None
    text_color: str | None = None
    hotspot_update_date: datetime
    click_date: datetime
    gcft_id: UUID4
    snap_id: UUID4

    _validate_reporting_id = field_validator("reporting_id", mode="before")(
        validate_reporting_id_required
    )
    _validate_hotspot_type_name = field_validator("hotspot_type_name", mode="before")(
        validate_hotspot_type_name_optional
    )
    _validate_hotspot_content = field_validator("hotspot_content", mode="before")(
        validate_hotspot_content_optional
    )
    _validate_hotspot_icon_name = field_validator("hotspot_icon_name", mode="before")(
        validate_hotspot_icon_name_optional
    )
    _validate_hotspot_name = field_validator("hotspot_name", mode="before")(
        validate_hotspot_name_optional
    )
    _validate_hotspot_user_icon_name = field_validator(
        "hotspot_user_icon_name", mode="before"
    )(validate_hotspot_user_icon_name_optional)
    _validate_linked_snap_name = field_validator("linked_snap_name", mode="before")(
        validate_linked_snap_name_optional
    )
    _validate_snap_file_name = field_validator("snap_file_name", mode="before")(
        validate_snap_file_name_optional
    )
    _validate_icon_color = field_validator("icon_color", mode="before")(
        validate_icon_color_optional
    )
    _validate_bg_color = field_validator("bg_color", mode="before")(
        validate_bg_color_optional
    )
    _validate_text_color = field_validator("text_color", mode="before")(
        validate_text_color_optional
    )


class GcftSnapHotspotclickCreate(GcftSnapHotspotclickBase):
    pass


class GcftSnapHotspotclickUpdate(BaseSchema):
    pass


class GcftSnapHotspotclickRead(GcftSnapHotspotclickBase, BaseSchemaRead):
    id: UUID4
