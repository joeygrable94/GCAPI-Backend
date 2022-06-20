from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Boolean, Column, DateTime, ForeignKey, String

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .gcft import GCFT  # noqa: F401
    from .gcft_snap import GCFTSnap  # noqa: F401


class GCFTSnapBrowserReport(TableBase):
    __tablename__ = "gcft_snap_browserreport"
    session_id = Column(String(36), nullable=False)
    browser = Column(String(255), nullable=True)
    browser_version = Column(String(255), nullable=True)
    platform = Column(String(255), nullable=True)
    platform_version = Column(String(255), nullable=True)
    desktop = Column(Boolean(), nullable=True)
    tablet = Column(Boolean(), nullable=True)
    mobile = Column(Boolean(), nullable=True)
    city = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    language = Column(String(255), nullable=True)
    visit_date = Column(DateTime(), nullable=False)

    # relationships
    gcft_id = Column(CHAR(36), ForeignKey("gcft.id"), nullable=False)
    snap_id = Column(CHAR(36), ForeignKey("gcft_snap.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str = f"GCFTSnapBrowserReport({self.session_id} on {self.visit_date}, browser={self.browser}, V.{self.browser_version})"
        return repr_str
