from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp, UUIDType

from app.db.base_class import Base
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_STORED
from app.services.permission import (
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
from app.utilities import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    from app.entities.go_ga4.model import GoAnalytics4Property
    from app.entities.go_ga4_stream.model import GoAnalytics4Stream
    from app.entities.go_gads.model import GoAdsProperty
    from app.entities.go_gsc.model import GoSearchConsoleProperty
    from app.entities.organization.model import Organization
    from app.entities.website_keywordcorpus.model import WebsiteKeywordCorpus
    from app.entities.website_page.model import WebsitePage
    from app.entities.website_pagespeedinsight.model import WebsitePageSpeedInsights


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
    organizations: Mapped[list["Organization"]] = relationship(
        "Organization", secondary="organization_website", back_populates="websites"
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
