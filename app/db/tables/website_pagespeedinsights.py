from decimal import Decimal
from typing import TYPE_CHECKING, Union
from uuid import UUID

from sqlalchemy import Column, Float, ForeignKey, String

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .website import Website  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsitePageSpeedInsights(TableBase):
    __tablename__: str = "website_pagespeedinsights"
    ps_grade: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    ps_value: Column[str] = Column(String(4), nullable=False, default="0%")
    fcp_grade: Column[Union[float, Decimal]] = Column(
        Float, nullable=False, default=0.0
    )
    fcp_value: Column[Union[float, Decimal]] = Column(
        Float, nullable=False, default=0.0
    )
    lcp_grade: Column[Union[float, Decimal]] = Column(
        Float, nullable=False, default=0.0
    )
    lcp_value: Column[Union[float, Decimal]] = Column(
        Float, nullable=False, default=0.0
    )
    cls_grade: Column[Union[float, Decimal]] = Column(
        Float, nullable=False, default=0.0
    )
    cls_value: Column[Union[float, Decimal]] = Column(
        Float, nullable=False, default=0.0
    )
    si_grade: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    si_value: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    tbt_grade: Column[Union[float, Decimal]] = Column(
        Float, nullable=False, default=0.0
    )
    tbt_value: Column[Union[float, Decimal]] = Column(
        Float, nullable=False, default=0.0
    )
    i_grade: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)
    i_value: Column[Union[float, Decimal]] = Column(Float, nullable=False, default=0.0)

    # relationships
    page_id: Column[UUID] = Column(GUID, ForeignKey("website_page.id"), nullable=False)
    website_id: Column[UUID] = Column(GUID, ForeignKey("website.id"), nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"PageSpeedInsights({self.id}, Site[{self.website_id}], Pg[{self.page_id}])"
        )
        return repr_str
