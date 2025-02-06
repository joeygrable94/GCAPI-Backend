from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.db.base_class import Base
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_STORED, DB_STR_URLPATH_MAXLEN_INPUT
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
    from app.entities.website_keywordcorpus.model import WebsiteKeywordCorpus
    from app.entities.website_pagespeedinsight.model import WebsitePageSpeedInsights


class WebsitePage(Base):
    __tablename__: str = "website_page"
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
    url: Mapped[str] = mapped_column(
        String(DB_STR_URLPATH_MAXLEN_INPUT),
        nullable=False,
        default="/",
    )
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=200)
    priority: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    last_modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    change_frequency: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    # relationships
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website.id"), index=True, nullable=False
    )
    website: Mapped["Website"] = relationship("Website", back_populates="pages")
    keywordcorpus: Mapped[list["WebsiteKeywordCorpus"]] = relationship(
        "WebsiteKeywordCorpus", back_populates="page", cascade="all, delete-orphan"
    )
    pagespeedinsights: Mapped[list["WebsitePageSpeedInsights"]] = relationship(
        "WebsitePageSpeedInsights", back_populates="page", cascade="all, delete-orphan"
    )

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
        repr_str: str = f"Page({self.id}, Site[{self.website_id}], Path[{self.url}])"
        return repr_str
