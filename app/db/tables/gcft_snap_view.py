from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, DateTime, ForeignKey, String

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .gcft import GCFT  # noqa: F401
    from .gcft_snap import GCFTSnap  # noqa: F401


class GCFTSnapView(TableBase):
    __tablename__ = "gcft_snap_view"
    session_id = Column(String(36), nullable=False)
    view_date = Column(DateTime(), nullable=False)

    # relationships
    gcft_id = Column(CHAR(36), ForeignKey("gcft.id"), nullable=False)
    snap_id = Column(CHAR(36), ForeignKey("gcft_snap.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str = f"GCFTSnapView({self.session_id} on {self.view_date})"
        return repr_str
