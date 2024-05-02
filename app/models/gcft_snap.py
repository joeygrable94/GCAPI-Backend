from typing import TYPE_CHECKING, Any, List, Optional

from pydantic import UUID4
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp  # type: ignore
from sqlalchemy_utils import UUIDType

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT, DB_STR_TINYTEXT_MAXLEN_INPUT

if TYPE_CHECKING:  # pragma: no cover
    from .file_asset import FileAsset  # noqa: F401
    from .gcft import Gcft  # noqa: F401
    from .gcft_snap_activeduration import GcftSnapActiveduration  # noqa: F401
    from .gcft_snap_browserreport import GcftSnapBrowserreport  # noqa: F401
    from .gcft_snap_hotspotclick import GcftSnapHotspotclick  # noqa: F401
    from .gcft_snap_trafficsource import GcftSnapTrafficsource  # noqa: F401
    from .gcft_snap_view import GcftSnapView  # noqa: F401
    from .geocoord import Geocoord  # noqa: F401


class GcftSnap(Base, Timestamp):
    __tablename__: str = "gcft_snap"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        primary_key=True,
        nullable=False,
        default=get_uuid(),
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
    file_asset_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("file_asset.id"), nullable=True, default=None
    )
    file_asset: Mapped[Optional["FileAsset"]] = relationship(
        "FileAsset", back_populates="gcft_snap"
    )
    geocoord_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("geocoord.id"), nullable=False
    )
    geotag: Mapped["Geocoord"] = relationship("Geocoord", back_populates="gcft_snaps")
    gcft_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft.id"), nullable=False
    )
    gcflytour: Mapped["Gcft"] = relationship("Gcft", back_populates="gcft_snaps")
    snap_views: Mapped[List["GcftSnapView"]] = relationship(
        "GcftSnapView", back_populates="gcft_snap"
    )
    active_durations: Mapped[List["GcftSnapActiveduration"]] = relationship(
        "GcftSnapActiveduration", back_populates="gcft_snap"
    )
    hotspot_clicks: Mapped[List["GcftSnapHotspotclick"]] = relationship(
        "GcftSnapHotspotclick", back_populates="gcft_snap"
    )
    traffic_sources: Mapped[List["GcftSnapTrafficsource"]] = relationship(
        "GcftSnapTrafficsource", back_populates="gcft_snap"
    )
    browser_reports: Mapped[List["GcftSnapBrowserreport"]] = relationship(
        "GcftSnapBrowserreport", back_populates="gcft_snap"
    )

    # represenation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"GcftSnap({self.snap_name}[{self.snap_slug}], \
            Tour[{self.gcft_id}], Coords[{self.geocoord_id}])"
        )
        return repr_str
