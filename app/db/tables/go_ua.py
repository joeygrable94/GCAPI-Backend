from typing import TYPE_CHECKING, Any, List, Optional
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, backref, relationship

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .go_ua_view import GoogleUniversalAnalyticsView  # noqa: F401
    from .website import Website  # noqa: F401


class GoogleUniversalAnalyticsProperty(TableBase):
    __tablename__: str = "go_ua"
    title: Mapped[str] = Column(String(255), nullable=False)
    tracking_id: Mapped[str] = Column(String(16), nullable=False)

    # relationships
    client_id: Mapped[UUID] = Column(GUID, ForeignKey("client.id"), nullable=False)
    website_id: Mapped[UUID] = Column(GUID, ForeignKey("website.id"), nullable=False)
    gua_views: Mapped[Optional[List[Any]]] = relationship(
        "GoogleUniversalAnalyticsView",
        backref=backref("go_ua", lazy="subquery"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoogleUniversalAnalytics(TrackingID[{self.tracking_id}] \
            for Client[{self.client_id}] Website[{self.website_id}])"
        return repr_str
