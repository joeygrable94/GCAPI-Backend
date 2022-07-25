from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import CHAR, Column, ForeignKey, String, Text
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .website_keywordcorpus import WebsiteKeywordCorpus  # noqa: F401
    from .website_pagespeedinsights import WebsitePageSpeedInsights  # noqa: F401


class WebsitePage(TableBase):
    __tablename__: str = "website_page"
    path: Column[str] = Column(Text, nullable=False, default="/")
    status: Column[str] = Column(String(24), nullable=False, default=200)

    # relationships
    website_id: Column[str] = Column(CHAR(36), ForeignKey("website.id"), nullable=False)
    sitemap_id: Column[Optional[str]] = Column(
        CHAR(36), ForeignKey("website_map.id"), nullable=True
    )
    keywordcorpus: Any = relationship(
        "WebsiteKeywordCorpus", backref=backref("website_page", lazy="noload")
    )
    pagespeedinsights: Any = relationship(
        "WebsitePageSpeedInsights", backref=backref("website_page", lazy="noload")
    )

    def __repr__(self) -> str:
        repr_str: str = f"Page({self.id}, Site[{self.website_id}], Path[{self.path}])"
        return repr_str
