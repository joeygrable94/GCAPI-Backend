from typing import TYPE_CHECKING, Any, List, Tuple

from pydantic import UUID4
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp  # type: ignore
from sqlalchemy_utils import UUIDType

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
from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_STORED

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .go_a4 import GoAnalytics4Property  # noqa: F401
    from .go_sc import GoSearchConsoleProperty  # noqa: F401
    from .website_keywordcorpus import WebsiteKeywordCorpus  # noqa: F401
    from .website_map import WebsiteMap  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401
    from .website_pagespeedinsights import WebsitePageSpeedInsights  # noqa: F401


class Website(Base, Timestamp):
    __tablename__: str = "website"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
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
    clients: Mapped[List["Client"]] = relationship(
        "Client", secondary="client_website", back_populates="websites"
    )
    sitemaps: Mapped[List["WebsiteMap"]] = relationship(
        "WebsiteMap", back_populates="website", cascade="all, delete-orphan"
    )
    pages: Mapped[List["WebsitePage"]] = relationship(
        "WebsitePage", back_populates="website", cascade="all, delete-orphan"
    )
    gsc_accounts: Mapped[List["GoSearchConsoleProperty"]] = relationship(
        "GoSearchConsoleProperty", back_populates="website"
    )
    ga4_accounts: Mapped[List["GoAnalytics4Property"]] = relationship(
        "GoAnalytics4Property", back_populates="website"
    )
    keywordcorpus: Mapped[List["WebsiteKeywordCorpus"]] = relationship(
        "WebsiteKeywordCorpus", back_populates="website"
    )
    pagespeedinsights: Mapped[List["WebsitePageSpeedInsights"]] = relationship(
        "WebsitePageSpeedInsights", back_populates="website"
    )

    # properties as methods
    def get_link(self) -> str:  # pragma: no cover
        return f"https://{self.domain}" if self.is_secure else f"http://{self.domain}"

    # ACL
    def __acl__(
        self,
    ) -> List[Tuple[AclAction, AclPrivilege, AclPermission]]:  # pragma: no cover
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
