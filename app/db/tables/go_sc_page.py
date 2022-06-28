from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, DateTime, Float, ForeignKey, Integer, Text

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .go_sc import GoogleSearchConsoleProperty  # noqa: F401


class GoogleSearchConsolePage(TableBase):
    __tablename__: str = "go_sc_page"
    keys: Column[str] = Column(Text, nullable=False)
    clicks: Column[int] = Column(Integer, nullable=False)
    impressions: Column[int] = Column(Integer, nullable=False)
    ctr: Column[float] = Column(Float(20), nullable=False)
    position: Column[float] = Column(Float(20), nullable=False)
    date_end: Column[datetime] = Column(DateTime(timezone=True), nullable=False)
    date_start: Column[datetime] = Column(DateTime(timezone=True), nullable=False)

    # relationships
    gsc_id: Column[str] = Column(CHAR(36), ForeignKey("go_sc.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = f"GoogleSearchConsolePage(GSCID[{self.gsc_id}], \
            C={self.clicks} I={self.impressions} CTR={self.ctr} Pos={self.position})"
        return repr_str
