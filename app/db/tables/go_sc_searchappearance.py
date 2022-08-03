from datetime import datetime
from typing import TYPE_CHECKING, Any

from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .go_sc import GoogleSearchConsoleProperty  # noqa: F401


class GoogleSearchConsoleSearchAppearance(TableBase):
    __tablename__: str = "go_sc_searchappearance"
    keys: Column[str] = Column(String(100), nullable=False)
    clicks: Column[int] = Column(Integer, nullable=False)
    impressions: Column[int] = Column(Integer, nullable=False)
    ctr: Column[Any] = Column(Float(20), nullable=False)
    position: Column[Any] = Column(Float(20), nullable=False)
    date_end: Column[datetime] = Column(DateTime(timezone=True), nullable=False)
    date_start: Column[datetime] = Column(DateTime(timezone=True), nullable=False)

    # relationships
    gsc_id: Column[str] = Column(GUID, ForeignKey("go_sc.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = f"GoogleSearchConsoleSearchAppearance(GSCID[{self.gsc_id}], \
            C={self.clicks} I={self.impressions} CTR={self.ctr} Pos={self.position})"
        return repr_str
