from datetime import datetime
from typing import TYPE_CHECKING

from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, DateTime, ForeignKey, String, Text

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .gcft import GCFT  # noqa: F401
    from .gcft_snap import GCFTSnap  # noqa: F401


class GCFTSnapTrafficSource(TableBase):
    __tablename__: str = "gcft_snap_trafficsource"
    session_id: Column[str] = Column(String(36), nullable=False)
    referrer: Column[str] = Column(Text, nullable=False)
    utm_campaign: Column[str] = Column(String(255), nullable=False)
    utm_content: Column[str] = Column(String(255), nullable=False)
    utm_medium: Column[str] = Column(String(255), nullable=False)
    utm_source: Column[str] = Column(String(255), nullable=False)
    utm_term: Column[str] = Column(String(255), nullable=False)
    visit_date: Column[datetime] = Column(DateTime(), nullable=False)

    # relationships
    gcft_id: Column[str] = Column(GUID, ForeignKey("gcft.id"), nullable=False)
    snap_id: Column[str] = Column(GUID, ForeignKey("gcft_snap.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = f"GCFTSnapTrafficSource({self.session_id} \
            on {self.visit_date}, referrer={self.active_seconds})"
        return repr_str
