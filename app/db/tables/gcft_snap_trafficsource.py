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


class GCFTSnapTrafficSource(TableBase):
    __tablename__: str = "gcft_snap_trafficsource"
    session_id: Mapped[str] = Column(String(36), nullable=False)
    referrer: Mapped[str] = Column(Text, nullable=False)
    utm_campaign: Mapped[str] = Column(String(255), nullable=False)
    utm_content: Mapped[str] = Column(String(255), nullable=False)
    utm_medium: Mapped[str] = Column(String(255), nullable=False)
    utm_source: Mapped[str] = Column(String(255), nullable=False)
    utm_term: Mapped[str] = Column(String(255), nullable=False)
    visit_date: Mapped[datetime] = Column(DateTime(), nullable=False)

    # relationships
    gcft_id: Mapped[UUID] = Column(GUID, ForeignKey("gcft.id"), nullable=False)
    snap_id: Mapped[UUID] = Column(GUID, ForeignKey("gcft_snap.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GCFTSnapTrafficSource({self.session_id} \
            on {self.visit_date}, referrer={self.referrer})"
        return repr_str
