from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import JSON, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import JSONType, UUIDType

from app.db.base_class import Base
from app.db.constants import DB_STR_16BIT_MAXLEN_STORED
from app.services.permission import (
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
from app.utilities.uuids import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    from app.entities.website.model import Website
    from app.entities.website_page.model import WebsitePage


class WebsitePageSpeedInsights(Base):
    __tablename__: str = "website_pagespeedinsights"
    __table_args__: dict = {"mysql_engine": "InnoDB"}
    __mapper_args__: dict = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        primary_key=True,
        nullable=False,
        default=get_uuid,
    )
    strategy: Mapped[str] = mapped_column(
        String(DB_STR_16BIT_MAXLEN_STORED), nullable=False, default="mobile"
    )
    score_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    grade_data: Mapped[JSON] = mapped_column(
        JSONType(),
        nullable=False,
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
    ) -> list[tuple[AclAction, AclPrivilege, AclPermission]]:  # pragma: no cover
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

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = "PageSpeedInsights(%s, Site[%s], Pg[%s], Str[%s])" % (
            self.id,
            self.website_id,
            self.page_id,
            self.strategy,
        )
        return repr_str
