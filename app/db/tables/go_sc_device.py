from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Union
from uuid import UUID

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .go_sc import GoogleSearchConsoleProperty  # noqa: F401


class GoogleSearchConsoleDevice(TableBase):
    __tablename__: str = "go_sc_device"
    keys: Column[str] = Column(String(100), nullable=False)
    clicks: Column[int] = Column(Integer, nullable=False)
    impressions: Column[int] = Column(Integer, nullable=False)
    ctr: Column[Union[float, Decimal]] = Column(Float(20), nullable=False)
    position: Column[Union[float, Decimal]] = Column(Float(20), nullable=False)
    date_end: Column[datetime] = Column(DateTime(timezone=True), nullable=False)
    date_start: Column[datetime] = Column(DateTime(timezone=True), nullable=False)

    # relationships
    gsc_id: Column[UUID] = Column(GUID, ForeignKey("go_sc.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoogleSearchConsoleDevice(GSCID[{self.gsc_id}], \
            C={self.clicks} I={self.impressions} CTR={self.ctr} Pos={self.position})"
        return repr_str
