from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp, UUIDType

from app.db.base_class import Base
from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT, DB_STR_TINYTEXT_MAXLEN_INPUT
from app.utilities import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    from app.entities.gcft.model import Gcft
    from app.entities.gcft_snap_active_duration.model import GcftSnapActiveduration
    from app.entities.gcft_snap_browser_report.model import GcftSnapBrowserreport
    from app.entities.gcft_snap_hotspot_click.model import GcftSnapHotspotclick
    from app.entities.gcft_snap_traffic_source.model import GcftSnapTrafficsource
    from app.entities.gcft_snap_view.model import GcftSnapView
    from app.entities.geocoord.model import Geocoord


class GcftSnap(Base, Timestamp):
    __tablename__: str = "gcft_snap"
    __table_args__: dict = {"mysql_engine": "InnoDB"}
    __mapper_args__: dict = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        primary_key=True,
        nullable=False,
        default=get_uuid,
    )
    snap_name: Mapped[str] = mapped_column(
        String(length=DB_STR_TINYTEXT_MAXLEN_INPUT),
        index=True,
        nullable=False,
    )
    snap_slug: Mapped[str] = mapped_column(
        String(length=DB_STR_16BIT_MAXLEN_INPUT),
        index=True,
        unique=True,
        nullable=False,
    )
    altitude: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
        default=0,
    )

    # relationships
    geocoord_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("geocoord.id"), nullable=False
    )
    geotag: Mapped["Geocoord"] = relationship("Geocoord", back_populates="gcft_snaps")
    gcft_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft.id"), nullable=False
    )
    gcflytour: Mapped["Gcft"] = relationship("Gcft", back_populates="gcft_snaps")
    snap_views: Mapped[list["GcftSnapView"]] = relationship(
        "GcftSnapView", back_populates="gcft_snap"
    )
    active_durations: Mapped[list["GcftSnapActiveduration"]] = relationship(
        "GcftSnapActiveduration", back_populates="gcft_snap"
    )
    hotspot_clicks: Mapped[list["GcftSnapHotspotclick"]] = relationship(
        "GcftSnapHotspotclick", back_populates="gcft_snap"
    )
    traffic_sources: Mapped[list["GcftSnapTrafficsource"]] = relationship(
        "GcftSnapTrafficsource", back_populates="gcft_snap"
    )
    browser_reports: Mapped[list["GcftSnapBrowserreport"]] = relationship(
        "GcftSnapBrowserreport", back_populates="gcft_snap"
    )

    # represenation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GcftSnap({self.snap_name}[{self.snap_slug}], \
            Tour[{self.gcft_id}], Coords[{self.geocoord_id}])"
        return repr_str
