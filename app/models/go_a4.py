from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp, UUIDType

from app.core.security.permissions import (
    AccessCreate,
    AccessCreateRelated,
    AccessDelete,
    AccessList,
    AccessListRelated,
    AccessListSelf,
    AccessRead,
    AccessReadRelated,
    AccessUpdate,
    AccessUpdateRelated,
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
from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT, DB_STR_TINYTEXT_MAXLEN_INPUT

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .go_a4_stream import GoAnalytics4Stream  # noqa: F401
    from .website import Website  # noqa: F401


class GoAnalytics4Property(Base, Timestamp):
    __tablename__: str = "go_a4"
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
    title: Mapped[str] = mapped_column(
        String(length=DB_STR_TINYTEXT_MAXLEN_INPUT),
        index=True,
        unique=True,
        nullable=False,
    )
    property_id: Mapped[str] = mapped_column(
        String(length=DB_STR_16BIT_MAXLEN_INPUT),
        index=True,
        unique=True,
        nullable=False,
    )

    # relationships
    platform_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("platform.id"), nullable=False
    )
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )
    client: Mapped["Client"] = relationship(back_populates="ga4_properties")
    websites: Mapped[list["Website"]] = relationship(
        "Website", secondary="website_go_a4", back_populates="ga4_properties"
    )
    ga4_streams: Mapped[list["GoAnalytics4Stream"]] = relationship(
        "GoAnalytics4Stream", back_populates="ga4_account"
    )

    # ACL
    def __acl__(
        self,
    ) -> list[tuple[AclAction, AclPrivilege, AclPermission]]:  # pragma: no cover
        return [
            # list
            (AclAction.allow, RoleAdmin, AccessList),
            (AclAction.allow, RoleManager, AccessList),
            (AclAction.allow, RoleEmployee, AccessListRelated),
            (AclAction.allow, RoleClient, AccessListSelf),
            # create
            (AclAction.allow, RoleAdmin, AccessCreate),
            (AclAction.allow, RoleManager, AccessCreate),
            (AclAction.allow, RoleEmployee, AccessCreateRelated),
            (AclAction.allow, RoleClient, AccessCreateRelated),
            # read
            (AclAction.allow, RoleAdmin, AccessRead),
            (AclAction.allow, RoleManager, AccessRead),
            (AclAction.allow, RoleEmployee, AccessReadRelated),
            (AclAction.allow, RoleClient, AccessReadRelated),
            # update
            (AclAction.allow, RoleAdmin, AccessUpdate),
            (AclAction.allow, RoleManager, AccessUpdate),
            (AclAction.allow, RoleEmployee, AccessUpdateRelated),
            (AclAction.allow, RoleClient, AccessUpdateRelated),
            # delete
            (AclAction.allow, RoleAdmin, AccessDelete),
            (AclAction.allow, RoleManager, AccessDelete),
        ]

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoAnalytics4Property(PropertyId[{self.property_id}] for Client[{self.client_id}])"  # noqa: F841, E501
        return repr_str
