from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.db.base_class import Base
from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT, DB_STR_TINYTEXT_MAXLEN_INPUT
from app.utilities.uuids import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    from app.entities.core_organization.model import Organization
    from app.entities.gcft_snap.model import GcftSnap
    from app.entities.gcft_snap_active_duration.model import GcftSnapActiveduration
    from app.entities.gcft_snap_browser_report.model import GcftSnapBrowserreport
    from app.entities.gcft_snap_hotspot_click.model import GcftSnapHotspotclick
    from app.entities.gcft_snap_traffic_source.model import GcftSnapTrafficsource
    from app.entities.gcft_snap_view.model import GcftSnapView


class Gcft(Base):
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
    organization_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("organization.id"), nullable=False
    )
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="gcflytours"
    )
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

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Gcft({self.group_name}[{self.group_slug}], Organization[{self.organization_id}])"
        return repr_str
