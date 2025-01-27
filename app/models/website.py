from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp, UUIDType

from app.core.security.permissions import (
    AccessCreate,
    AccessDelete,
    AccessList,
    AccessRead,
    AccessUpdate,
    AclAction,
    AclPermission,
    AclPrivilege,
    RoleAdmin,
    RoleManager,
    RoleUser,
)
from app.core.utilities import get_uuid
from app.db.base_class import Base
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_STORED

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .go_a4 import GoAnalytics4Property  # noqa: F401
    from .go_a4_stream import GoAnalytics4Stream  # noqa: F401
    from .go_ads import GoAdsProperty  # noqa: F401
    from .go_sc import GoSearchConsoleProperty  # noqa: F401
    from .website_keywordcorpus import WebsiteKeywordCorpus  # noqa: F401
    from .website_map import WebsiteMap  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401
    from .website_pagespeedinsights import WebsitePageSpeedInsights  # noqa: F401


class Website(Base, Timestamp):
    __tablename__: str = "website"
    __table_args__: dict = {"mysql_engine": "InnoDB"}
    __mapper_args__: dict = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid,
    )
    domain: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    is_secure: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    # relationships
    clients: Mapped[list["Client"]] = relationship(
        "Client", secondary="client_website", back_populates="websites"
    )
    sitemaps: Mapped[list["WebsiteMap"]] = relationship(
        "WebsiteMap", back_populates="website", cascade="all, delete-orphan"
    )
    pages: Mapped[list["WebsitePage"]] = relationship(
        "WebsitePage", back_populates="website", cascade="all, delete-orphan"
    )
    ga4_properties: Mapped[list["GoAnalytics4Property"]] = relationship(
        "GoAnalytics4Property", secondary="website_go_a4", back_populates="websites"
    )
    ga4_streams: Mapped[list["GoAnalytics4Stream"]] = relationship(
        "GoAnalytics4Stream", back_populates="website"
    )
    gads_accounts: Mapped[list["GoAdsProperty"]] = relationship(
        "GoAdsProperty", secondary="website_go_ads", back_populates="websites"
    )
    gsc_properties: Mapped[list["GoSearchConsoleProperty"]] = relationship(
        "GoSearchConsoleProperty",
        back_populates="website",
    )
    keywordcorpus: Mapped[list["WebsiteKeywordCorpus"]] = relationship(
        "WebsiteKeywordCorpus", back_populates="website"
    )
    pagespeedinsights: Mapped[list["WebsitePageSpeedInsights"]] = relationship(
        "WebsitePageSpeedInsights", back_populates="website"
    )

    # properties as methods
    def get_link(self) -> str:  # pragma: no cover
        return f"https://{self.domain}" if self.is_secure else f"http://{self.domain}"

    # ACL
    def __acl__(
        self,
    ) -> list[tuple[AclAction, AclPrivilege, AclPermission]]:  # pragma: no cover
        return [
            # list
            (AclAction.allow, RoleUser, AccessList),
            # create
            (AclAction.allow, RoleAdmin, AccessCreate),
            (AclAction.allow, RoleManager, AccessCreate),
            # read
            (AclAction.allow, RoleUser, AccessRead),
            # update
            (AclAction.allow, RoleUser, AccessUpdate),
            # delete
            (AclAction.allow, RoleUser, AccessDelete),
        ]

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Website({self.id}, Domain[{self.domain}])"
        return repr_str
