from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.db.base_class import Base
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_STORED
from app.utilities.uuids import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    from app.entities.gcft.model import Gcft
    from app.entities.gcft_snap.model import GcftSnap


class GcftSnapBrowserreport(Base):
    __tablename__: str = "gcft_snap_browserreport"
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
    browser: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    browser_version: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    platform: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    platform_version: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    desktop: Mapped[bool] = mapped_column(Boolean(), nullable=True)
    tablet: Mapped[bool] = mapped_column(Boolean(), nullable=True)
    mobile: Mapped[bool] = mapped_column(Boolean(), nullable=True)
    city: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    country: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    state: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    language: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    visit_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # relationships
    gcft_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft.id"), nullable=False
    )
    gcflytour: Mapped["Gcft"] = relationship("Gcft", back_populates="browser_reports")
    snap_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft_snap.id"), nullable=False
    )
    gcft_snap: Mapped["GcftSnap"] = relationship(
        "GcftSnap", back_populates="browser_reports"
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GcftSnapBrowserreport({self.session_id} \
            on {self.visit_date}, browser={self.browser}, V.{self.browser_version})"
        return repr_str
