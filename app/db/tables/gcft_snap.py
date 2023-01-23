from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, backref, relationship

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
    snap_name: Mapped[str] = Column(String(255), nullable=False)
    snap_slug: Mapped[str] = Column(String(12), nullable=False)
    altitude: Mapped[int] = Column(Integer, nullable=False)

    # relationships
    geocoord_id: Mapped[UUID] = Column(GUID, ForeignKey("geocoord.id"), nullable=True)
    gcft_id: Mapped[UUID] = Column(GUID, ForeignKey("gcft.id"), nullable=False)
    snap_views: Mapped[Optional[List["GCFTSnapView"]]] = relationship(
        "GCFTSnapView", backref=backref("gcft_snap", lazy="noload")
    )
    active_durations: Mapped[Optional[List["GCFTSnapActiveDuration"]]] = relationship(
        "GCFTSnapActiveDuration", backref=backref("gcft_snap", lazy="noload")
    )
    hotspot_clicks: Mapped[Optional[List["GCFTSnapHotspotClick"]]] = relationship(
        "GCFTSnapHotspotClick", backref=backref("gcft_snap", lazy="noload")
    )
    traffic_sources: Mapped[Optional[List["GCFTSnapTrafficSource"]]] = relationship(
        "GCFTSnapTrafficSource", backref=backref("gcft_snap", lazy="noload")
    )
    browser_reports: Mapped[Optional[List["GCFTSnapBrowserReport"]]] = relationship(
        "GCFTSnapBrowserReport", backref=backref("gcft_snap", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GCFTSnap({self.snap_name}[{self.snap_slug}], \
            Tour[{self.gcft_id}], Coords[{self.geocoord_id}])"
        return repr_str
