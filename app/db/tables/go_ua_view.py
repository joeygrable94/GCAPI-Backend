from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .go_ua import GoogleUniversalAnalyticsProperty  # noqa: F401


class GoogleUniversalAnalyticsView(TableBase):
    __tablename__: str = "go_ua_view"
    title: Column[str] = Column(String(255), nullable=False)
    view_id: Column[str] = Column(String(16), nullable=False)

    # relationships
    gua_id: Column[UUID] = Column(GUID, ForeignKey("go_ua.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoogleUniversalAnalyticsView({self.title} \
            View[{self.view_id}] for GUA Property[{self.gua_id}])"
        return repr_str
