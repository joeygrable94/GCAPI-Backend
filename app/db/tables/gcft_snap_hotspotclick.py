from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .gcft import GCFT  # noqa: F401
    from .gcft_snap import GCFTSnap  # noqa: F401


class GCFTSnapHotspotClick(TableBase):
    __tablename__: str = "gcft_snap_hotspotclick"
    session_id: Mapped[str] = Column(String(36), nullable=False)
    reporting_id: Mapped[str] = Column(String(255), nullable=True)
    hotspot_type_name: Mapped[str] = Column(String(32), nullable=True)
    hotspot_content: Mapped[str] = Column(Text, nullable=True)
    hotspot_icon_name: Mapped[str] = Column(String(255), nullable=True)
    hotspot_name: Mapped[str] = Column(String(255), nullable=True)
    hotspot_user_icon_name: Mapped[str] = Column(String(255), nullable=True)
    linked_snap_name: Mapped[str] = Column(String(255), nullable=True)
    snap_file_name: Mapped[str] = Column(String(255), nullable=True)
    icon_color: Mapped[str] = Column(String(20), nullable=True)
    bg_color: Mapped[str] = Column(String(20), nullable=True)
    text_color: Mapped[str] = Column(String(20), nullable=True)
    hotspot_update_date: Mapped[datetime] = Column(DateTime(), nullable=False)
    click_date: Mapped[datetime] = Column(DateTime(), nullable=False)

    # relationships
    gcft_id: Mapped[UUID] = Column(GUID, ForeignKey("gcft.id"), nullable=False)
    snap_id: Mapped[UUID] = Column(GUID, ForeignKey("gcft_snap.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GCFTSnapHotspotClick({self.session_id} \
            on {self.click_date}, type={self.hotspot_type_name})"
        return repr_str
