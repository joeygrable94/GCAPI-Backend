from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp, UUIDType

from app.core.utilities import get_uuid
from app.db.base_class import Base
from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT, DB_STR_TINYTEXT_MAXLEN_INPUT

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .gcft_snap import GcftSnap  # noqa: F401
    from .gcft_snap_activeduration import GcftSnapActiveduration  # noqa: F401
    from .gcft_snap_browserreport import GcftSnapBrowserreport  # noqa: F401
    from .gcft_snap_hotspotclick import GcftSnapHotspotclick  # noqa: F401
    from .gcft_snap_trafficsource import GcftSnapTrafficsource  # noqa: F401
    from .gcft_snap_view import GcftSnapView  # noqa: F401


class Gcft(Base, Timestamp):
    __tablename__: str = "gcft"
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
    group_name: Mapped[str] = mapped_column(
        String(length=DB_STR_TINYTEXT_MAXLEN_INPUT),
        index=True,
        nullable=False,
    )
    group_slug: Mapped[str] = mapped_column(
        String(length=DB_STR_16BIT_MAXLEN_INPUT),
        index=True,
        nullable=False,
    )

    # relationships
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )
    client: Mapped["Client"] = relationship("Client", back_populates="gcflytours")
    gcft_snaps: Mapped[list["GcftSnap"]] = relationship(
        "GcftSnap", back_populates="gcflytour"
    )
    snap_views: Mapped[list["GcftSnapView"]] = relationship(
        "GcftSnapView", back_populates="gcflytour"
    )
    active_durations: Mapped[list["GcftSnapActiveduration"]] = relationship(
        "GcftSnapActiveduration", back_populates="gcflytour"
    )
    hotspot_clicks: Mapped[list["GcftSnapHotspotclick"]] = relationship(
        "GcftSnapHotspotclick", back_populates="gcflytour"
    )
    traffic_sources: Mapped[list["GcftSnapTrafficsource"]] = relationship(
        "GcftSnapTrafficsource", back_populates="gcflytour"
    )
    browser_reports: Mapped[list["GcftSnapBrowserreport"]] = relationship(
        "GcftSnapBrowserreport", back_populates="gcflytour"
    )

    # represenation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"Gcft({self.group_name}[{self.group_slug}], Client[{self.client_id}])"
        )
        return repr_str
