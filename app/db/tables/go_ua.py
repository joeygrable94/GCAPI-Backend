from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401
    from .go_ua_view import GoogleUniversalAnalyticsView  # noqa: F401
    from .website import Website  # noqa: F401


class GoogleUniversalAnalyticsProperty(TableBase):
    __tablename__ = "go_ua"
    title = Column(String(255), nullable=False)
    tracking_id = Column(String(16), nullable=False)

    # relationships
    client_id = Column(CHAR(36), ForeignKey("client.id"), nullable=False)
    website_id = Column(CHAR(36), ForeignKey("website.id"), nullable=False)
    gua_views = relationship(
        "GoogleUniversalAnalyticsView",
        backref=backref("go_ua", lazy="subquery"),
    )

    def __repr__(self) -> str:
        repr_str = f"GoogleUniversalAnalytics(TrackingID[{self.tracking_id}] for Client[{self.client_id}] Website[{self.website_id}])"
        return repr_str
