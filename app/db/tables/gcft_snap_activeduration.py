from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, DateTime, ForeignKey, Integer, String

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .gcft import GCFT  # noqa: F401
    from .gcft_snap import GCFTSnap  # noqa: F401


class GCFTSnapActiveDuration(TableBase):
    __tablename__ = "gcft_snap_activeduration"
    session_id = Column(String(36), nullable=False)
    active_seconds = Column(Integer(), nullable=False)
    view_date = Column(DateTime(), nullable=False)

    # relationships
    gcft_id = Column(CHAR(36), ForeignKey("gcft.id"), nullable=False)
    snap_id = Column(CHAR(36), ForeignKey("gcft_snap.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str = f"GCFTSnapActiveDuration({self.session_id} on {self.view_date}, seconds={self.active_seconds})"
        return repr_str
