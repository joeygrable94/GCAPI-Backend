from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import UUID4
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .website import Website  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsitePageSpeedInsights(Base):
    __tablename__: str = "website_pagespeedinsights"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.current_timestamp(),
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
    strategy: Mapped[str] = mapped_column(String(16), nullable=False, default="mobile")
    ps_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    ps_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    ps_value: Mapped[str] = mapped_column(String(4), nullable=False, default="0%")
    ps_unit: Mapped[str] = mapped_column(String(16), nullable=False, default="percent")
    fcp_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    fcp_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    fcp_value: Mapped[str] = mapped_column(Float, nullable=False, default=0.0)
    fcp_unit: Mapped[str] = mapped_column(
        String(16), nullable=False, default="miliseconds"
    )
    lcp_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=25)
    lcp_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    lcp_value: Mapped[str] = mapped_column(Float, nullable=False, default=0.0)
    lcp_unit: Mapped[str] = mapped_column(
        String(16), nullable=False, default="miliseconds"
    )
    cls_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=15)
    cls_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    cls_value: Mapped[str] = mapped_column(Float, nullable=False, default=0.0)
    cls_unit: Mapped[str] = mapped_column(
        String(16), nullable=False, default="unitless"
    )
    si_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    si_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    si_value: Mapped[str] = mapped_column(Float, nullable=False, default=0.0)
    si_unit: Mapped[str] = mapped_column(
        String(16), nullable=False, default="miliiseconds"
    )
    tbt_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    tbt_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    tbt_value: Mapped[str] = mapped_column(Float, nullable=False, default=0.0)
    tbt_unit: Mapped[str] = mapped_column(
        String(16), nullable=False, default="miliseconds"
    )

    # relationships
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website.id"), nullable=False
    )
    website: Mapped["Website"] = relationship(
        "Website", back_populates="pagespeedinsights"
    )
    page_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website_page.id"), nullable=False
    )
    page: Mapped["WebsitePage"] = relationship(
        "WebsitePage", back_populates="pagespeedinsights"
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = "PageSpeedInsights(%s, Site[%s], Pg[%s], Str[%s])" % (
            self.id,
            self.website_id,
            self.page_id,
            self.strategy,
        )
        return repr_str
