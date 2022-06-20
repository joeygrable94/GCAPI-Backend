from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, Float, ForeignKey

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .website import Website  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsitePageSpeedInsights(TableBase):
    __tablename__ = "website_pagespeedinsights"
    ps_grade = Column(Float)
    ps_value = Column(Float)
    fcp_grade = Column(Float)
    fcp_value = Column(Float)
    lcp_grade = Column(Float)
    lcp_value = Column(Float)
    cls_grade = Column(Float)
    cls_value = Column(Float)
    si_grade = Column(Float)
    si_value = Column(Float)
    tbt_grade = Column(Float)
    tbt_value = Column(Float)
    i_grade = Column(Float)
    i_value = Column(Float)

    # relationships
    page_id = Column(CHAR(36), ForeignKey("website_page.id"), nullable=False)
    website_id = Column(CHAR(36), ForeignKey("website.id"), nullable=False)

    def __repr__(self):
        repr_str = (
            f"PageSpeedInsights({self.id}, Site[{self.website_id}], Pg[{self.page_id}])"
        )
        return repr_str
