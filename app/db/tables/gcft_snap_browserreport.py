from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .gcft import GCFT  # noqa: F401
    from .gcft_snap import GCFTSnap  # noqa: F401


class GCFTSnapBrowserReport(TableBase):
    __tablename__: str = "gcft_snap_browserreport"
    session_id: Mapped[str] = Column(String(36), nullable=False)
    browser: Mapped[str] = Column(String(255), nullable=True)
    browser_version: Mapped[str] = Column(String(255), nullable=True)
    platform: Mapped[str] = Column(String(255), nullable=True)
    platform_version: Mapped[str] = Column(String(255), nullable=True)
    desktop: Mapped[bool] = Column(Boolean(), nullable=True)
    tablet: Mapped[bool] = Column(Boolean(), nullable=True)
    mobile: Mapped[bool] = Column(Boolean(), nullable=True)
    city: Mapped[str] = Column(String(255), nullable=True)
    country: Mapped[str] = Column(String(255), nullable=True)
    state: Mapped[str] = Column(String(255), nullable=True)
    language: Mapped[str] = Column(String(255), nullable=True)
    visit_date: Mapped[datetime] = Column(DateTime(), nullable=False)

    # relationships
    gcft_id: Mapped[UUID] = Column(GUID, ForeignKey("gcft.id"), nullable=False)
    snap_id: Mapped[UUID] = Column(GUID, ForeignKey("gcft_snap.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GCFTSnapBrowserReport({self.session_id} \
            on {self.visit_date}, browser={self.browser}, V.{self.browser_version})"
        return repr_str
