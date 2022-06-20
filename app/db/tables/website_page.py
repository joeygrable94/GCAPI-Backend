from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey, String, Text
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .website_keywordcorpus import WebsiteKeywordCorpus  # noqa: F401
    from .website_pagespeedinsights import \
        WebsitePageSpeedInsights  # noqa: F401


class WebsitePage(TableBase):
    __tablename__ = "website_page"
    path = Column(Text)
    status = Column(String(24))

    # relationships
    website_id = Column(CHAR(36), ForeignKey("website.id"), nullable=False)
    sitemap_id = Column(CHAR(36), ForeignKey("website_map.id"))
    keywordcorpus = relationship(
        "WebsiteKeywordCorpus", backref=backref("website_page", lazy="noload")
    )
    pagespeedinsights = relationship(
        "WebsitePageSpeedInsights", backref=backref("website_page", lazy="noload")
    )

    def __repr__(self):
        repr_str = f"Page({self.id}, Site[{self.website_id}], Path[{self.path}])"
        return repr_str
