from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Tuple

from pydantic import UUID4
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.security.permissions import (
    AccessCreate,
    AccessDelete,
    AccessList,
    AccessRead,
    AccessUpdate,
    AclAction,
    AclPermission,
    AclPrivilege,
    RoleUser,
)
from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import DB_STR_16BIT_MAXLEN_STORED

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
    strategy: Mapped[str] = mapped_column(
        String(DB_STR_16BIT_MAXLEN_STORED), nullable=False, default="mobile"
    )
    ps_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    ps_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    ps_value: Mapped[str] = mapped_column(
        String(DB_STR_16BIT_MAXLEN_STORED), nullable=False, default="0%"
    )
    ps_unit: Mapped[str] = mapped_column(
        String(DB_STR_16BIT_MAXLEN_STORED), nullable=False, default="percent"
    )
    fcp_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    fcp_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    fcp_value: Mapped[str] = mapped_column(Float, nullable=False, default=0.0)
    fcp_unit: Mapped[str] = mapped_column(
        String(DB_STR_16BIT_MAXLEN_STORED), nullable=False, default="miliseconds"
    )
    lcp_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=25)
    lcp_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    lcp_value: Mapped[str] = mapped_column(Float, nullable=False, default=0.0)
    lcp_unit: Mapped[str] = mapped_column(
        String(DB_STR_16BIT_MAXLEN_STORED), nullable=False, default="miliseconds"
    )
    cls_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=15)
    cls_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    cls_value: Mapped[str] = mapped_column(Float, nullable=False, default=0.0)
    cls_unit: Mapped[str] = mapped_column(
        String(DB_STR_16BIT_MAXLEN_STORED), nullable=False, default="unitless"
    )
    si_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    si_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    si_value: Mapped[str] = mapped_column(Float, nullable=False, default=0.0)
    si_unit: Mapped[str] = mapped_column(
        String(DB_STR_16BIT_MAXLEN_STORED), nullable=False, default="miliiseconds"
    )
    tbt_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    tbt_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    tbt_value: Mapped[str] = mapped_column(Float, nullable=False, default=0.0)
    tbt_unit: Mapped[str] = mapped_column(
        String(DB_STR_16BIT_MAXLEN_STORED), nullable=False, default="miliseconds"
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

    # ACL
    def __acl__(
        self,
    ) -> List[Tuple[AclAction, AclPrivilege, AclPermission]]:  # pragma: no cover
        return [
            # list
            (AclAction.allow, RoleUser, AccessList),
            # create
            (AclAction.allow, RoleUser, AccessCreate),
            # read
            (AclAction.allow, RoleUser, AccessRead),
            # update
            (AclAction.allow, RoleUser, AccessUpdate),
            # delete
            (AclAction.allow, RoleUser, AccessDelete),
        ]

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = "PageSpeedInsights(%s, Site[%s], Pg[%s], Str[%s])" % (
            self.id,
            self.website_id,
            self.page_id,
            self.strategy,
        )
        return repr_str
