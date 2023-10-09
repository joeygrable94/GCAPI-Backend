from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4

from app.db.acls import GcftSnapACL
from app.db.validators import (
    ValidateSchemaAltitudeOptional,
    ValidateSchemaAltitudeRequired,
    ValidateSchemaSnapNameOptional,
    ValidateSchemaSnapNameRequired,
    ValidateSchemaSnapSlugRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class GcftSnapBase(
    ValidateSchemaSnapNameRequired,
    ValidateSchemaSnapSlugRequired,
    ValidateSchemaAltitudeRequired,
):
    snap_name: str
    snap_slug: str
    altitude: int
    gcft_id: UUID4
    geocoord_id: UUID4
    file_asset_id: Optional[UUID4] = None


class GcftSnapCreate(GcftSnapBase):
    pass


class GcftSnapUpdate(
    ValidateSchemaSnapNameOptional,
    ValidateSchemaAltitudeOptional,
):
    snap_name: Optional[str] = None
    altitude: Optional[int] = None
    gcft_id: Optional[UUID4] = None
    geocoord_id: Optional[UUID4] = None
    file_asset_id: Optional[UUID4] = None


class GcftSnapRead(GcftSnapACL, GcftSnapBase, BaseSchemaRead):
    id: UUID4


# relationships
class GcftSnapReadRelations(GcftSnapRead):
    snap_views: Optional[List["GcftSnapViewRead"]] = None
    active_durations: Optional[List["GcftSnapActivedurationRead"]] = None
    hotspot_clicks: Optional[List["GcftSnapHotspotclickRead"]] = None
    traffic_sources: Optional[List["GcftSnapTrafficsourceRead"]] = None
    browser_reports: Optional[List["GcftSnapBrowserreportRead"]] = None


from app.schemas.gcft_snap_activeduration import (  # noqa: E402, E501
    GcftSnapActivedurationRead,
)
from app.schemas.gcft_snap_browserreport import (  # noqa: E402, E501
    GcftSnapBrowserreportRead,
)
from app.schemas.gcft_snap_hotspotclick import GcftSnapHotspotclickRead  # noqa: E402
from app.schemas.gcft_snap_trafficsource import (  # noqa: E402, E501
    GcftSnapTrafficsourceRead,
)
from app.schemas.gcft_snap_view import GcftSnapViewRead  # noqa: E402

GcftSnapReadRelations.model_rebuild()