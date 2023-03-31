from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .website_keywordcorpus import WebsiteKeywordCorpus  # noqa: F401
    from .website_pagespeedinsights import WebsitePageSpeedInsights  # noqa: F401


class WebsitePage(Base):
    __tablename__: str = "website_page"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        index=True,
        nullable=False,
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    url: Mapped[str] = mapped_column(Text, nullable=False, default="/")
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=200)
    priority: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    last_modified: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    change_frequency: Mapped[str] = mapped_column(
        String(64), nullable=True, default=None
    )

    # relationships
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website.id"), nullable=False
    )
    sitemap_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website_map.id"), nullable=True
    )
    keywordcorpus: Mapped[UUID4] = relationship(
        "WebsiteKeywordCorpus", backref=backref("website_keywordcorpus", lazy="noload")
    )
    pagespeedinsights: Mapped[UUID4] = relationship(
        "WebsitePageSpeedInsights", backref=backref("website_page", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Page({self.id}, Site[{self.website_id}], Path[{self.url}])"
        return repr_str
