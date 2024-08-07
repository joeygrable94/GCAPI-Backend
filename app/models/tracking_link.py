from typing import TYPE_CHECKING, Any, List, Tuple

from pydantic import UUID4
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp  # type: ignore
from sqlalchemy_utils import UUIDType

from app.core.security.permissions import (
    AccessCreate,
    AccessDelete,
    AccessDeleteRelated,
    AccessList,
    AccessRead,
    AccessReadRelated,
    AccessUpdate,
    AccessUpdateRelated,
    AclAction,
    AclPermission,
    AclPrivilege,
    RoleAdmin,
    RoleManager,
    RoleUser,
)
from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_STORED, DB_STR_URLPATH_MAXLEN_STORED

if TYPE_CHECKING:  # pragma: no cover
    from .client_report import Client  # noqa: F401


class TrackingLink(Base, Timestamp):
    __tablename__: str = "tracking_link"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        primary_key=True,
        nullable=False,
        default=get_uuid(),
    )
    url_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    url: Mapped[str] = mapped_column(
        String(DB_STR_URLPATH_MAXLEN_STORED),
        nullable=False,
        default="https://getcommunity.com/?UTMLINK",
    )
    utm_campaign: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    utm_content: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    utm_medium: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    utm_source: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    utm_term: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=True,
    )

    # relationships
    clients: Mapped[List["Client"]] = relationship(
        "Client", secondary="client_tracking_link", back_populates="tracking_links"
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
            (AclAction.allow, RoleAdmin, AccessRead),
            (AclAction.allow, RoleManager, AccessRead),
            (AclAction.allow, RoleUser, AccessReadRelated),
            # update
            (AclAction.allow, RoleAdmin, AccessUpdate),
            (AclAction.allow, RoleManager, AccessUpdate),
            (AclAction.allow, RoleUser, AccessUpdateRelated),
            # delete
            (AclAction.allow, RoleAdmin, AccessDelete),
            (AclAction.allow, RoleManager, AccessDelete),
            (AclAction.allow, RoleUser, AccessDeleteRelated),
        ]

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"TrackingLink({self.url})"
        return repr_str
