from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .go_sc import GoogleSearchConsoleProperty  # noqa: F401


class GoogleSearchConsoleSearchAppearance(TableBase):
    __tablename__: str = "go_sc_searchappearance"
    keys: Mapped[str] = Column(String(100), nullable=False)
    clicks: Mapped[int] = Column(Integer, nullable=False)
    impressions: Mapped[int] = Column(Integer, nullable=False)
    ctr: Mapped[float] = Column(Float(20), nullable=False)
    position: Mapped[float] = Column(Float(20), nullable=False)
    date_end: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)
    date_start: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)

    # relationships
    gsc_id: Mapped[UUID] = Column(GUID, ForeignKey("go_sc.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoogleSearchConsoleSearchAppearance(GSCID[{self.gsc_id}], \
            C={self.clicks} I={self.impressions} CTR={self.ctr} Pos={self.position})"
        return repr_str
