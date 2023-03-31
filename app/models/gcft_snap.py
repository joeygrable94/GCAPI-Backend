from datetime import datetime
from typing import TYPE_CHECKING, List

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .gcft import GCFT  # noqa: F401
    from .gcft_snap_activeduration import GCFTSnapActiveDuration  # noqa: F401
    from .gcft_snap_browserreport import GCFTSnapBrowserReport  # noqa: F401
    from .gcft_snap_hotspotclick import GCFTSnapHotspotClick  # noqa: F401
    from .gcft_snap_trafficsource import GCFTSnapTrafficSource  # noqa: F401
    from .gcft_snap_view import GCFTSnapView  # noqa: F401
    from .geocoord import GeoCoord  # noqa: F401


class GCFTSnap(Base):
    __tablename__: str = "gcft_snap"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        index=True,
        nullable=False,
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    snap_name: Mapped[str] = mapped_column(String(255), nullable=False)
    snap_slug: Mapped[str] = mapped_column(String(12), nullable=False)
    altitude: Mapped[int] = mapped_column(Integer, nullable=False)

    # relationships
    geocoord_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("geocoord.id"), nullable=True
    )
    gcft_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft.id"), nullable=False
    )
    snap_views: Mapped[List["GCFTSnapView"]] = relationship(
        "GCFTSnapView", backref=backref("gcft_snap", lazy="noload")
    )
    active_durations: Mapped[List["GCFTSnapActiveDuration"]] = relationship(
        "GCFTSnapActiveDuration", backref=backref("gcft_snap", lazy="noload")
    )
    hotspot_clicks: Mapped[List["GCFTSnapHotspotClick"]] = relationship(
        "GCFTSnapHotspotClick", backref=backref("gcft_snap", lazy="noload")
    )
    traffic_sources: Mapped[List["GCFTSnapTrafficSource"]] = relationship(
        "GCFTSnapTrafficSource", backref=backref("gcft_snap", lazy="noload")
    )
    browser_reports: Mapped[List["GCFTSnapBrowserReport"]] = relationship(
        "GCFTSnapBrowserReport", backref=backref("gcft_snap", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GCFTSnap({self.snap_name}[{self.snap_slug}], \
            Tour[{self.gcft_id}], Coords[{self.geocoord_id}])"
        return repr_str
