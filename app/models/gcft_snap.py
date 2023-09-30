from datetime import datetime
from typing import TYPE_CHECKING, Any, List

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .gcft import Gcft  # noqa: F401
    from .gcft_snap_activeduration import GcftSnapActiveduration  # noqa: F401
    from .gcft_snap_browserreport import GcftSnapBrowserreport  # noqa: F401
    from .gcft_snap_hotspotclick import GcftSnapHotspotclick  # noqa: F401
    from .gcft_snap_trafficsource import GcftSnapTrafficsource  # noqa: F401
    from .gcft_snap_view import GcftSnapView  # noqa: F401
    from .geocoord import Geocoord  # noqa: F401


class GcftSnap(Base):
    __tablename__: str = "gcft_snap"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.current_timestamp(),
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
    snap_name: Mapped[str] = mapped_column(String(255), nullable=False)
    snap_slug: Mapped[str] = mapped_column(
        String(12), nullable=False, unique=True, primary_key=True
    )
    altitude: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # relationships
    gcft_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft.id"), nullable=False
    )
    file_asset_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("file_asset.id"), nullable=True, default=None
    )
    geocoord_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("geocoord.id"), nullable=False
    )
    snap_views: Mapped[List["GcftSnapView"]] = relationship(
        "GcftSnapView", backref=backref("gcft_snap", lazy="noload")
    )
    active_durations: Mapped[List["GcftSnapActiveduration"]] = relationship(
        "GcftSnapActiveduration", backref=backref("gcft_snap", lazy="noload")
    )
    hotspot_clicks: Mapped[List["GcftSnapHotspotclick"]] = relationship(
        "GcftSnapHotspotclick", backref=backref("gcft_snap", lazy="noload")
    )
    traffic_sources: Mapped[List["GcftSnapTrafficsource"]] = relationship(
        "GcftSnapTrafficsource", backref=backref("gcft_snap", lazy="noload")
    )
    browser_reports: Mapped[List["GcftSnapBrowserreport"]] = relationship(
        "GcftSnapBrowserreport", backref=backref("gcft_snap", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GcftSnap({self.snap_name}[{self.snap_slug}], \
            Tour[{self.gcft_id}], Coords[{self.geocoord_id}])"
        return repr_str
