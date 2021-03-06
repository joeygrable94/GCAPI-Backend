from datetime import datetime
from typing import TYPE_CHECKING, Optional

from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, DateTime, ForeignKey, String, Text

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .gcft import GCFT  # noqa: F401
    from .gcft_snap import GCFTSnap  # noqa: F401


class GCFTSnapHotspotClick(TableBase):
    __tablename__: str = "gcft_snap_hotspotclick"
    session_id: Column[str] = Column(String(36), nullable=False)
    reporting_id: Column[Optional[str]] = Column(String(255), nullable=True)
    hotspot_type_name: Column[Optional[str]] = Column(String(32), nullable=True)
    hotspot_content: Column[Optional[str]] = Column(Text, nullable=True)
    hotspot_icon_name: Column[Optional[str]] = Column(String(255), nullable=True)
    hotspot_name: Column[Optional[str]] = Column(String(255), nullable=True)
    hotspot_user_icon_name: Column[Optional[str]] = Column(String(255), nullable=True)
    linked_snap_name: Column[Optional[str]] = Column(String(255), nullable=True)
    snap_file_name: Column[Optional[str]] = Column(String(255), nullable=True)
    icon_color: Column[Optional[str]] = Column(String(20), nullable=True)
    bg_color: Column[Optional[str]] = Column(String(20), nullable=True)
    text_color: Column[Optional[str]] = Column(String(20), nullable=True)
    hotspot_update_date: Column[datetime] = Column(DateTime(), nullable=False)
    click_date: Column[datetime] = Column(DateTime(), nullable=False)

    # relationships
    gcft_id: Column[str] = Column(GUID, ForeignKey("gcft.id"), nullable=False)
    snap_id: Column[str] = Column(GUID, ForeignKey("gcft_snap.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = f"GCFTSnapHotspotClick({self.session_id} \
            on {self.click_date}, type={self.hotspot_type_name})"
        return repr_str
