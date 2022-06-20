from typing import TYPE_CHECKING

from sqlalchemy import (CHAR, Column, DateTime, Float, ForeignKey, Integer,
                        String)

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .go_sc import GoogleSearchConsoleProperty  # noqa: F401


class GoogleSearchConsoleDevice(TableBase):
    __tablename__ = "go_sc_device"
    keys = Column(String(100), nullable=False)
    clicks = Column(Integer, nullable=False)
    impressions = Column(Integer, nullable=False)
    ctr = Column(Float(20), nullable=False)
    position = Column(Float(20), nullable=False)
    date_end = Column(DateTime(timezone=True), nullable=False)
    date_start = Column(DateTime(timezone=True), nullable=False)

    # relationships
    gsc_id = Column(CHAR(36), ForeignKey("go_sc.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str = f"GoogleSearchConsoleDevice(GSCID[{self.gsc_id}], C={self.clicks} I={self.impressions} CTR={self.ctr} Pos={self.position})"
        return repr_str
