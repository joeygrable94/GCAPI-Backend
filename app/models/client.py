from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp, UUIDType

from app.core.security.permissions import (
    AccessCreate,
    AccessDelete,
    AccessDeleteSelf,
    AccessList,
    AccessRead,
    AccessReadRelated,
    AccessReadSelf,
    AccessUpdate,
    AccessUpdateRelated,
    AccessUpdateSelf,
    AclAction,
    AclPermission,
    AclPrivilege,
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
)
from app.core.utilities import get_uuid
from app.db.base_class import Base
from app.db.constants import (
    DB_STR_64BIT_MAXLEN_INPUT,
    DB_STR_DESC_MAXLEN_INPUT,
    DB_STR_TINYTEXT_MAXLEN_INPUT,
)

if TYPE_CHECKING:  # pragma: no cover
    from .client_styleguide import ClientStyleguide  # noqa: F401
    from .gcft import Gcft  # noqa: F401
    from .go_a4 import GoAnalytics4Property  # noqa: F401
    from .go_ads import GoAdsProperty  # noqa: F401
    from .go_sc import GoSearchConsoleProperty  # noqa: F401
    from .platform import Platform  # noqa: F401
    from .tracking_link import TrackingLink  # noqa: F401
    from .user import User  # noqa: F401
    from .website import Website  # noqa: F401


class Client(Base, Timestamp):
    __tablename__: str = "client"
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
    slug: Mapped[str] = mapped_column(
        String(length=DB_STR_64BIT_MAXLEN_INPUT),
        index=True,
        unique=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(length=DB_STR_TINYTEXT_MAXLEN_INPUT),
        index=True,
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(length=DB_STR_DESC_MAXLEN_INPUT), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=True,
    )

    # relationships
    users: Mapped[list["User"]] = relationship(
        "User", secondary="user_client", back_populates="clients"
    )
    styleguides: Mapped[list["ClientStyleguide"]] = relationship(
        "ClientStyleguide", back_populates="client", cascade="all, delete-orphan"
    )
    websites: Mapped[list["Website"]] = relationship(
        secondary="client_website", back_populates="clients", cascade="all, delete"
    )
    tracking_links: Mapped[list["TrackingLink"]] = relationship(
        "TrackingLink", back_populates="client"
    )
    platforms: Mapped[list["Platform"]] = relationship(
        "Platform", secondary="client_platform", back_populates="clients"
    )
    ga4_properties: Mapped[list["GoAnalytics4Property"]] = relationship(
        "GoAnalytics4Property", back_populates="client", cascade="all, delete-orphan"
    )
    gads_accounts: Mapped[list["GoAdsProperty"]] = relationship(
        "GoAdsProperty", back_populates="client", cascade="all, delete-orphan"
    )
    gsc_properties: Mapped[list["GoSearchConsoleProperty"]] = relationship(
        "GoSearchConsoleProperty", back_populates="client", cascade="all, delete-orphan"
    )
    gcflytours: Mapped[list["Gcft"]] = relationship(
        "Gcft", back_populates="client", cascade="all, delete-orphan"
    )

    # ACL
    def __acl__(
        self,
    ) -> list[tuple[AclAction, AclPrivilege, AclPermission]]:  # pragma: no cover
        return [
            # list
            (AclAction.allow, RoleAdmin, AccessList),
            (AclAction.allow, RoleManager, AccessList),
            (AclAction.allow, RoleClient, AccessList),
            (AclAction.allow, RoleEmployee, AccessList),
            # create
            (AclAction.allow, RoleAdmin, AccessCreate),
            (AclAction.allow, RoleManager, AccessCreate),
            # read
            (AclAction.allow, RoleAdmin, AccessRead),
            (AclAction.allow, RoleManager, AccessRead),
            (AclAction.allow, RoleClient, AccessReadSelf),
            (AclAction.allow, RoleEmployee, AccessReadRelated),
            # update
            (AclAction.allow, RoleAdmin, AccessUpdate),
            (AclAction.allow, RoleManager, AccessUpdate),
            (AclAction.allow, RoleClient, AccessUpdateSelf),
            (AclAction.allow, RoleEmployee, AccessUpdateRelated),
            # delete
            (AclAction.allow, RoleAdmin, AccessDelete),
            (AclAction.allow, RoleClient, AccessDeleteSelf),
        ]

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Client({self.title}, since {self.created})"
        return repr_str
