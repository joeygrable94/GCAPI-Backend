from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp, UUIDType

from app.core.security.permissions import (
    AccessCreate,
    AccessDelete,
    AccessList,
    AccessListRelated,
    AccessListSelf,
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
    from .client import Client  # noqa: F401


class Platform(Base, Timestamp):
    __tablename__: str = "platform"
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
    clients: Mapped[list["Client"]] = relationship(
        "Client", secondary="client_platform", back_populates="platforms"
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
            # read
            (AclAction.allow, RoleAdmin, AccessRead),
            (AclAction.allow, RoleManager, AccessRead),
            (AclAction.allow, RoleEmployee, AccessReadRelated),
            (AclAction.allow, RoleClient, AccessReadSelf),
            # update
            (AclAction.allow, RoleAdmin, AccessUpdate),
            (AclAction.allow, RoleManager, AccessUpdate),
            (AclAction.allow, RoleEmployee, AccessUpdateRelated),
            (AclAction.allow, RoleClient, AccessUpdateSelf),
            # delete
            (AclAction.allow, RoleAdmin, AccessDelete),
        ]

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Platform({self.title})"
        return repr_str
