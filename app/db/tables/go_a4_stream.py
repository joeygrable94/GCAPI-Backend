from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey, String

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .go_a4 import GoogleAnalytics4Property  # noqa: F401


class GoogleAnalytics4Stream(TableBase):
    __tablename__: str = "go_a4_stream"
    title: Column[str] = Column(String(255), nullable=False)
    stream_id: Column[str] = Column(String(16), nullable=False)

    # relationships
    ga4_id: Column[str] = Column(CHAR(36), ForeignKey("go_a4.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = f"GoogleAnalytics4Stream({self.title} \
            Stream[{self.stream_id}] for GA4 Property[{self.ga4_id}])"
        return repr_str
