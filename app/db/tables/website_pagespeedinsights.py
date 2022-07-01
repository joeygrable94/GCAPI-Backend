from typing import TYPE_CHECKING, Any

from sqlalchemy import CHAR, Column, Float, ForeignKey

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .website import Website  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsitePageSpeedInsights(TableBase):
    __tablename__: str = "website_pagespeedinsights"
    ps_grade: Column[Any] = Column(Float, nullable=False, default=0.0)
    ps_value: Column[Any] = Column(Float, nullable=False, default=0.0)
    fcp_grade: Column[Any] = Column(Float, nullable=False, default=0.0)
    fcp_value: Column[Any] = Column(Float, nullable=False, default=0.0)
    lcp_grade: Column[Any] = Column(Float, nullable=False, default=0.0)
    lcp_value: Column[Any] = Column(Float, nullable=False, default=0.0)
    cls_grade: Column[Any] = Column(Float, nullable=False, default=0.0)
    cls_value: Column[Any] = Column(Float, nullable=False, default=0.0)
    si_grade: Column[Any] = Column(Float, nullable=False, default=0.0)
    si_value: Column[Any] = Column(Float, nullable=False, default=0.0)
    tbt_grade: Column[Any] = Column(Float, nullable=False, default=0.0)
    tbt_value: Column[Any] = Column(Float, nullable=False, default=0.0)
    i_grade: Column[Any] = Column(Float, nullable=False, default=0.0)
    i_value: Column[Any] = Column(Float, nullable=False, default=0.0)

    # relationships
    page_id = Column(CHAR(36), ForeignKey("website_page.id"), nullable=False)
    website_id = Column(CHAR(36), ForeignKey("website.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = (
            f"PageSpeedInsights({self.id}, Site[{self.website_id}], Pg[{self.page_id}])"
        )
        return repr_str
