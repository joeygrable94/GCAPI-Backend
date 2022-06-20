from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Boolean, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401
    from .website import Website  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsiteMap(TableBase):
    __tablename__ = "website_map"
    title = Column(String(255), nullable=False, default="unnamed")
    filename = Column(String(120), nullable=False, default="sample.xml")
    processed = Column(Boolean(), nullable=False, default=False)

    # relationships
    website_id = Column(CHAR(36), ForeignKey("website.id"), nullable=False)
    pages = relationship("WebsitePage", backref=backref("website_map", lazy="noload"))

    def __repr__(self):
        repr_str = (
            f"WebsiteMap({self.title}, Site[{self.website_id}], File[{self.filename}])"
        )
        return repr_str
