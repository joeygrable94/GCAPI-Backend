from decimal import Decimal
from typing import TYPE_CHECKING, Union
from uuid import UUID

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .website import Website  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsitePageSpeedInsights(TableBase):
    __tablename__: str = "website_pagespeedinsights"
    strategy: Column[str] = Column(String(16), nullable=False, default="mobile")
    ps_weight: Column[int] = Column(Integer, nullable=False, default=100)
    ps_grade: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    ps_value: Column[str] = Column(String(4), nullable=False, default="0%")
    ps_unit: Column[str] = Column(String(16), nullable=False, default="percent")
    fcp_weight: Column[int] = Column(Integer, nullable=False, default=10)
    fcp_grade: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    fcp_value: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    fcp_unit: Column[str] = Column(String(16), nullable=False, default="miliseconds")
    lcp_weight: Column[int] = Column(Integer, nullable=False, default=25)
    lcp_grade: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    lcp_value: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    lcp_unit: Column[str] = Column(String(16), nullable=False, default="miliseconds")
    cls_weight: Column[int] = Column(Integer, nullable=False, default=15)
    cls_grade: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    cls_value: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    cls_unit: Column[str] = Column(String(16), nullable=False, default="unitless")
    si_weight: Column[int] = Column(Integer, nullable=False, default=10)
    si_grade: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    si_value: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    si_unit: Column[str] = Column(String(16), nullable=False, default="miliiseconds")
    tbt_weight: Column[int] = Column(Integer, nullable=False, default=30)
    tbt_grade: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    tbt_value: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    tbt_unit: Column[str] = Column(String(16), nullable=False, default="miliseconds")
    i_weight: Column[int] = Column(Integer, nullable=False, default=10)
    i_grade: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    i_value: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    i_unit: Column[str] = Column(String(16), nullable=False, default="miliseconds")

    # relationships
    page_id: Column[UUID] = Column(GUID, ForeignKey("website_page.id"), nullable=False)
    website_id: Column[UUID] = Column(GUID, ForeignKey("website.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            "PageSpeedInsights(%s, Site[%s], Pg[%s], Str[%s])" % (
                self.id,
                self.website_id,
                self.page_id,
                self.strategy,
            )
        )
        return repr_str
