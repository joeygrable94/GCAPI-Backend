from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .gcft import GCFT  # noqa: F401
    from .gcft_snap import GCFTSnap  # noqa: F401


class GCFTSnapView(TableBase):
    __tablename__: str = "gcft_snap_view"
    session_id: Mapped[str] = Column(String(36), nullable=False)
    view_date: Mapped[datetime] = Column(DateTime(), nullable=False)

    # relationships
    gcft_id: Mapped[UUID] = Column(GUID, ForeignKey("gcft.id"), nullable=False)
    snap_id: Mapped[UUID] = Column(GUID, ForeignKey("gcft_snap.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GCFTSnapView({self.session_id} on {self.view_date})"
        return repr_str
