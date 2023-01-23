from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .go_ua import GoogleUniversalAnalyticsProperty  # noqa: F401


class GoogleUniversalAnalyticsView(TableBase):
    __tablename__: str = "go_ua_view"
    title: Mapped[str] = Column(String(255), nullable=False)
    view_id: Mapped[str] = Column(String(16), nullable=False)

    # relationships
    gua_id: Mapped[UUID] = Column(GUID, ForeignKey("go_ua.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoogleUniversalAnalyticsView({self.title} \
            View[{self.view_id}] for GUA Property[{self.gua_id}])"
        return repr_str
