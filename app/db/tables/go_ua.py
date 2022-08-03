from typing import TYPE_CHECKING, Any

from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401
    from .go_ua_view import GoogleUniversalAnalyticsView  # noqa: F401
    from .website import Website  # noqa: F401


class GoogleUniversalAnalyticsProperty(TableBase):
    __tablename__: str = "go_ua"
    title: Column[str] = Column(String(255), nullable=False)
    tracking_id: Column[str] = Column(String(16), nullable=False)

    # relationships
    client_id: Column[str] = Column(GUID, ForeignKey("client.id"), nullable=False)
    website_id: Column[str] = Column(GUID, ForeignKey("website.id"), nullable=False)
    gua_views: Any = relationship(
        "GoogleUniversalAnalyticsView",
        backref=backref("go_ua", lazy="subquery"),
    )

    def __repr__(self) -> str:
        repr_str: str = f"GoogleUniversalAnalytics(TrackingID[{self.tracking_id}] \
            for Client[{self.client_id}] Website[{self.website_id}])"
        return repr_str
