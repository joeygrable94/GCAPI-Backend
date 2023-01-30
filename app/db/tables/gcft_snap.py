from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .gcft import GCFT  # noqa: F401
    from .gcft_snap_activeduration import GCFTSnapActiveDuration  # noqa: F401
    from .gcft_snap_browserreport import GCFTSnapBrowserReport  # noqa: F401
    from .gcft_snap_hotspotclick import GCFTSnapHotspotClick  # noqa: F401
    from .gcft_snap_trafficsource import GCFTSnapTrafficSource  # noqa: F401
    from .gcft_snap_view import GCFTSnapView  # noqa: F401
    from .geocoord import GeoCoord  # noqa: F401


class GCFTSnap(TableBase):
    __tablename__: str = "gcft_snap"
    snap_name: Column[str] = Column(String(255), nullable=False)
    snap_slug: Column[str] = Column(String(12), nullable=False)
    altitude: Column[int] = Column(Integer, nullable=False)

    # relationships
    geocoord_id: Column[Optional[UUID]] = Column(
        GUID, ForeignKey("geocoord.id"), nullable=True
    )
    gcft_id: Column[UUID] = Column(GUID, ForeignKey("gcft.id"), nullable=False)
    snap_views: Column[Optional[List["GCFTSnapView"]]] = relationship(  # type: ignore
        "GCFTSnapView", backref=backref("gcft_snap", lazy="noload")
    )
    active_durations: Column[
        Optional[List["GCFTSnapActiveDuration"]]
    ] = relationship(  # type: ignore
        "GCFTSnapActiveDuration", backref=backref("gcft_snap", lazy="noload")
    )
    hotspot_clicks: Column[
        Optional[List["GCFTSnapHotspotClick"]]
    ] = relationship(  # type: ignore
        "GCFTSnapHotspotClick", backref=backref("gcft_snap", lazy="noload")
    )
    traffic_sources: Column[
        Optional[List["GCFTSnapTrafficSource"]]
    ] = relationship(  # type: ignore
        "GCFTSnapTrafficSource", backref=backref("gcft_snap", lazy="noload")
    )
    browser_reports: Column[
        Optional[List["GCFTSnapBrowserReport"]]
    ] = relationship(  # type: ignore
        "GCFTSnapBrowserReport", backref=backref("gcft_snap", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GCFTSnap({self.snap_name}[{self.snap_slug}], \
            Tour[{self.gcft_id}], Coords[{self.geocoord_id}])"
        return repr_str
