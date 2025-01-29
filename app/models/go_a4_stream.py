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
    from .go_a4 import GoAnalytics4Property  # noqa: F401
    from .website import Website  # noqa: F401


class GoAnalytics4Stream(Base, Timestamp):
    __tablename__: str = "go_a4_stream"
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
    stream_id: Mapped[str] = mapped_column(
        String(length=DB_STR_16BIT_MAXLEN_INPUT),
        index=True,
        unique=True,
        nullable=False,
    )
    measurement_id: Mapped[str] = mapped_column(
        String(length=DB_STR_16BIT_MAXLEN_INPUT),
        index=True,
        unique=True,
        nullable=False,
    )

    # relationships
    ga4_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("go_a4.id"), nullable=False
    )
    ga4_account: Mapped["GoAnalytics4Property"] = relationship(
        "GoAnalytics4Property", back_populates="ga4_streams"
    )
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website.id"), nullable=False
    )
    website: Mapped["Website"] = relationship(back_populates="ga4_streams")

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

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoAnalytics4Stream({self.title} Stream[{self.stream_id}] for GA4 Property[{self.ga4_id}] and Website[{self.website_id}])"  # noqa: F841, E501
        return repr_str
