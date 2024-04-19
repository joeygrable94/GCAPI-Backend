from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import UUID4
from sqlalchemy import BLOB, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import DB_STR_32BIT_MAXLEN_STORED, DB_STR_TINYTEXT_MAXLEN_STORED

if TYPE_CHECKING:  # pragma: no cover
    from .gcft import Gcft  # noqa: F401
    from .gcft_snap import GcftSnap  # noqa: F401


class GcftSnapHotspotclick(Base):
    __tablename__: str = "gcft_snap_hotspotclick"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        primary_key=True,
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
    session_id: Mapped[UUID4] = mapped_column(UUIDType(binary=False), nullable=False)
    reporting_id: Mapped[str] = mapped_column(
        String(DB_STR_32BIT_MAXLEN_STORED), nullable=True
    )
    hotspot_type_name: Mapped[str] = mapped_column(
        String(DB_STR_32BIT_MAXLEN_STORED), nullable=True
    )
    hotspot_content: Mapped[str] = mapped_column(BLOB, nullable=True)
    hotspot_icon_name: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    hotspot_name: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    hotspot_user_icon_name: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    linked_snap_name: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    snap_file_name: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    icon_color: Mapped[str] = mapped_column(
        String(DB_STR_32BIT_MAXLEN_STORED), nullable=True
    )
    bg_color: Mapped[str] = mapped_column(
        String(DB_STR_32BIT_MAXLEN_STORED), nullable=True
    )
    text_color: Mapped[str] = mapped_column(
        String(DB_STR_32BIT_MAXLEN_STORED), nullable=True
    )
    hotspot_update_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    click_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    # relationships
    gcft_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft.id"), nullable=False
    )
    gcflytour: Mapped["Gcft"] = relationship("Gcft", back_populates="hotspot_clicks")
    snap_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("gcft_snap.id"), nullable=False
    )
    gcft_snap: Mapped["GcftSnap"] = relationship(
        "GcftSnap", back_populates="hotspot_clicks"
    )

    # represenation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"GcftSnapHotspotclick({self.session_id} \
            on {self.click_date}, type={self.hotspot_type_name})"
        )
        return repr_str
