from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401
    from .go_a4_stream import GoogleAnalytics4Stream  # noqa: F401
    from .website import Website  # noqa: F401


class GoogleAnalytics4Property(TableBase):
    __tablename__ = "go_a4"
    title = Column(String(255), nullable=False)
    measurement_id = Column(String(16), nullable=False)
    property_id = Column(String(16), nullable=False)

    # relationships
    client_id = Column(CHAR(36), ForeignKey("client.id"), nullable=False)
    website_id = Column(CHAR(36), ForeignKey("website.id"), nullable=False)
    ga4_streams = relationship(
        "GoogleAnalytics4Stream",
        backref=backref("go_a4", lazy="subquery"),
    )

    def __repr__(self) -> str:
        repr_str = f"GoogleAnalytics4Property(MeasurementID[{self.measurement_id}] for Client[{self.client_id}] Website[{self.website_id}])"
        return repr_str
