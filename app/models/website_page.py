from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from pydantic import UUID4
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import StringEncryptedType  # type: ignore
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine  # type: ignore

from app.core.config import settings
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

if TYPE_CHECKING:  # pragma: no cover
    from .website import Website  # noqa: F401
    from .website_keywordcorpus import WebsiteKeywordCorpus  # noqa: F401
    from .website_map import WebsiteMap  # noqa: F401
    from .website_pagespeedinsights import WebsitePageSpeedInsights  # noqa: F401


class WebsitePage(Base):
    __tablename__: str = "website_page"
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
    url: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            key=settings.api.encryption_key,
            engine=AesEngine,
            padding="pkcs5",
            length=2048,
        ),
        nullable=False,
        default="/",
    )
    status: Mapped[int] = mapped_column(
        StringEncryptedType(
            Integer,
            key=settings.api.encryption_key,
            engine=AesEngine,
            padding="oneandzeroes",
        ),
        nullable=False,
        default=200,
    )
    priority: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    last_modified: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    change_frequency: Mapped[str] = mapped_column(String(64), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        StringEncryptedType(
            Boolean,
            key=settings.api.encryption_key,
            engine=AesEngine,
            padding="zeroes",
        ),
        nullable=False,
        default=True,
    )

    # relationships
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website.id"), index=True, nullable=False
    )
    website: Mapped["Website"] = relationship("Website", back_populates="pages")
    sitemap_id: Mapped[Optional[UUID4]] = mapped_column(
        UUIDType(binary=False), ForeignKey("website_map.id"), index=True, nullable=True
    )
    sitemap: Mapped[Optional["WebsiteMap"]] = relationship(
        "WebsiteMap", back_populates="pages"
    )
    keywordcorpus: Mapped[List["WebsiteKeywordCorpus"]] = relationship(
        "WebsiteKeywordCorpus", back_populates="page", cascade="all, delete-orphan"
    )
    pagespeedinsights: Mapped[List["WebsitePageSpeedInsights"]] = relationship(
        "WebsitePageSpeedInsights", back_populates="page", cascade="all, delete-orphan"
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
        repr_str: str = f"Page({self.id}, Site[{self.website_id}], Path[{self.url}])"
        return repr_str
