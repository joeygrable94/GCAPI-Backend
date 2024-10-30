from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from pydantic import UUID4
from sqlalchemy import Boolean, ForeignKey, String
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
    RoleUser,
)
from app.core.utilities import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import DB_STR_URLPATH_MAXLEN_STORED

if TYPE_CHECKING:  # pragma: no cover
    from .website import Website  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsiteMap(Base, Timestamp):
    __tablename__: str = "website_map"
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
    url: Mapped[str] = mapped_column(
        String(DB_STR_URLPATH_MAXLEN_STORED),
        nullable=False,
        default="https://getcommunity.com/sitemap_index.xml",
    )
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    # relationships
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website.id"), nullable=False
    )
    website: Mapped["Website"] = relationship("Website", back_populates="sitemaps")
    pages: Mapped[Optional[List["WebsitePage"]]] = relationship(
        "WebsitePage", back_populates="sitemap", cascade="all, delete-orphan"
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
        repr_str: str = f"WebsiteMap({self.url}, Site[{self.website_id}])"
        return repr_str
