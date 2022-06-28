from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, Float, ForeignKey

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .website import Website  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsitePageSpeedInsights(TableBase):
    __tablename__: str = "website_pagespeedinsights"
    ps_grade: Column[float] = Column(Float)
    ps_value: Column[float] = Column(Float)
    fcp_grade: Column[float] = Column(Float)
    fcp_value: Column[float] = Column(Float)
    lcp_grade: Column[float] = Column(Float)
    lcp_value: Column[float] = Column(Float)
    cls_grade: Column[float] = Column(Float)
    cls_value: Column[float] = Column(Float)
    si_grade: Column[float] = Column(Float)
    si_value: Column[float] = Column(Float)
    tbt_grade: Column[float] = Column(Float)
    tbt_value: Column[float] = Column(Float)
    i_grade: Column[float] = Column(Float)
    i_value: Column[float] = Column(Float)

    # relationships
    page_id = Column(CHAR(36), ForeignKey("website_page.id"), nullable=False)
    website_id = Column(CHAR(36), ForeignKey("website.id"), nullable=False)

    def __repr__(self) -> str:
        repr_str: str = (
            f"PageSpeedInsights({self.id}, Site[{self.website_id}], Pg[{self.page_id}])"
        )
        return repr_str
