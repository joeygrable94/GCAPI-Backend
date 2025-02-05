from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp, UUIDType

from app.db.base_class import Base
from app.db.constants import (
    DB_STR_16BIT_MAXLEN_INPUT,
    DB_STR_TINYTEXT_MAXLEN_INPUT,
    DB_STR_URLPATH_MAXLEN_INPUT,
)
from app.services.permission import (
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
from app.utilities import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    from app.entities.organization.model import Organization


class TrackingLink(Base, Timestamp):
    __tablename__: str = "tracking_link"
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
    url_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    url: Mapped[str] = mapped_column(
        String(DB_STR_URLPATH_MAXLEN_INPUT),
        nullable=False,
        default="https://getcommunity.com/path-to-destination/?UTMLINK",
    )
    scheme: Mapped[str] = mapped_column(
        String(DB_STR_16BIT_MAXLEN_INPUT),
        nullable=False,
        default="http",
    )
    domain: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_INPUT),
        nullable=False,
        default="getcommunity.com",
    )
    destination: Mapped[str] = mapped_column(
        String(DB_STR_URLPATH_MAXLEN_INPUT),
        nullable=False,
        default="https://getcommunity.com/path-to-destination/",
    )
    url_path: Mapped[str] = mapped_column(
        String(DB_STR_URLPATH_MAXLEN_INPUT),
        nullable=False,
        default="/path-to-destination/",
    )
    utm_campaign: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_INPUT), nullable=True
    )
    utm_medium: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_INPUT), nullable=True
    )
    utm_source: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_INPUT), nullable=True
    )
    utm_content: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_INPUT), nullable=True
    )
    utm_term: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_INPUT), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=True,
    )

    # relationships
    organization_id: Mapped[UUID4 | None] = mapped_column(
        UUIDType(binary=False), ForeignKey("organization.id"), nullable=True
    )
    organization: Mapped["Organization"] = relationship(back_populates="tracking_links")

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
