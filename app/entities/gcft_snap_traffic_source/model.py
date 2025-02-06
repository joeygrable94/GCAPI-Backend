from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.db.base_class import Base
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_STORED, DB_STR_URLPATH_MAXLEN_STORED
from app.utilities.uuids import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    from app.entities.gcft.model import Gcft
    from app.entities.gcft_snap.model import GcftSnap


class GcftSnapTrafficsource(Base):
    __tablename__: str = "gcft_snap_trafficsource"
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
    session_id: Mapped[UUID4] = mapped_column(UUIDType(binary=False), nullable=False)
    referrer: Mapped[str] = mapped_column(
        String(DB_STR_URLPATH_MAXLEN_STORED),
        nullable=False,
        default="/",
    )
    utm_campaign: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    utm_content: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    utm_medium: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    utm_source: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    utm_term: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    visit_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # relationships
    gcft_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft.id"), nullable=False
    )
    gcflytour: Mapped["Gcft"] = relationship("Gcft", back_populates="traffic_sources")
    snap_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft_snap.id"), nullable=False
    )
    gcft_snap: Mapped["GcftSnap"] = relationship(
        "GcftSnap", back_populates="traffic_sources"
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GcftSnapTrafficsource({self.session_id} \
            on {self.visit_date}, referrer={self.referrer})"
        return repr_str
