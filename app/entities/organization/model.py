from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp, UUIDType

from app.db.base_class import Base
from app.db.constants import (
    DB_STR_64BIT_MAXLEN_INPUT,
    DB_STR_DESC_MAXLEN_INPUT,
    DB_STR_TINYTEXT_MAXLEN_INPUT,
)
from app.services.permission import (
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
from app.utilities import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    from app.entities.gcft.model import Gcft
    from app.entities.go_ga4.model import GoAnalytics4Property
    from app.entities.go_gads.model import GoAdsProperty
    from app.entities.go_gsc.model import GoSearchConsoleProperty
    from app.entities.organization_styleguide.model import OrganizationStyleguide
    from app.entities.platform.model import Platform
    from app.entities.tracking_link.model import TrackingLink
    from app.entities.user.model import User
    from app.entities.website.model import Website


class Organization(Base, Timestamp):
    __tablename__: str = "organization"
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
        "User", secondary="user_organization", back_populates="organizations"
    )
    styleguides: Mapped[list["OrganizationStyleguide"]] = relationship(
        "OrganizationStyleguide",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    websites: Mapped[list["Website"]] = relationship(
        secondary="organization_website",
        back_populates="organizations",
        cascade="all, delete",
    )
    tracking_links: Mapped[list["TrackingLink"]] = relationship(
        "TrackingLink", back_populates="organization"
    )
    platforms: Mapped[list["Platform"]] = relationship(
        "Platform", secondary="organization_platform", back_populates="organizations"
    )
    ga4_properties: Mapped[list["GoAnalytics4Property"]] = relationship(
        "GoAnalytics4Property",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    gads_accounts: Mapped[list["GoAdsProperty"]] = relationship(
        "GoAdsProperty", back_populates="organization", cascade="all, delete-orphan"
    )
    gsc_properties: Mapped[list["GoSearchConsoleProperty"]] = relationship(
        "GoSearchConsoleProperty",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    gcflytours: Mapped[list["Gcft"]] = relationship(
        "Gcft", back_populates="organization", cascade="all, delete-orphan"
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
        repr_str: str = f"Organization({self.title}, since {self.created})"
        return repr_str
