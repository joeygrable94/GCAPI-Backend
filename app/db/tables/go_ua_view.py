from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey, String

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .go_ua import GoogleUniversalAnalyticsProperty  # noqa: F401


class GoogleUniversalAnalyticsView(TableBase):
    __tablename__: str = "go_ua_view"
    title = Column(String(255), nullable=False)
    view_id = Column(String(16), nullable=False)

    # relationships
    gua_id = Column(CHAR(36), ForeignKey("go_ua.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = f"GoogleUniversalAnalyticsView({self.title} \
            View[{self.view_id}] for GUA Property[{self.gua_id}])"
        return repr_str
