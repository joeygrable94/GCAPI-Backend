from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .website_keywordcorpus import WebsiteKeywordCorpus  # noqa: F401
    from .website_pagespeedinsights import WebsitePageSpeedInsights  # noqa: F401


class WebsitePage(TableBase):
    __tablename__: str = "website_page"
    path: Column[str] = Column(Text, nullable=False, default="/")
    status: Column[str] = Column(String(24), nullable=False, default=200)

    # relationships
    website_id: Column[UUID] = Column(GUID, ForeignKey("website.id"), nullable=False)
    sitemap_id: Column[Optional[UUID]] = Column(
        GUID, ForeignKey("website_map.id"), nullable=True
    )
    keywordcorpus: Column[
        Optional[List["WebsiteKeywordCorpus"]]
    ] = relationship(  # type: ignore
        "WebsiteKeywordCorpus", backref=backref("website_page", lazy="noload")
    )
    pagespeedinsights: Column[
        Optional[List["WebsitePageSpeedInsights"]]
    ] = relationship(  # type: ignore
        "WebsitePageSpeedInsights", backref=backref("website_page", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Page({self.id}, Site[{self.website_id}], Path[{self.path}])"
        return repr_str
