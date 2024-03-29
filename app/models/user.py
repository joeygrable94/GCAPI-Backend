from datetime import datetime
from typing import TYPE_CHECKING, Any, Tuple

from pydantic import UUID4
from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.security.permissions import (
    AccessCreate,
    AccessDelete,
    AccessDeleteSelf,
    AccessList,
    AccessRead,
    AccessReadSelf,
    AccessUpdate,
    AccessUpdateSelf,
    AclAction,
    AclPermission,
    AclPrivilege,
    RoleAdmin,
    RoleManager,
    RoleUser,
)
from app.core.utilities.uuids import get_random_username  # type: ignore
from app.core.utilities.uuids import get_uuid
from app.db.base_class import Base
from app.db.custom_types import Scopes

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .file_asset import FileAsset  # noqa: F401
    from .ipaddress import Ipaddress  # noqa: F401
    from .note import Note  # noqa: F401


class User(Base):
    __tablename__: str = "user"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.current_timestamp(),
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
    auth_id: Mapped[str] = mapped_column(
        String(255), unique=True, primary_key=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, default=get_random_username()
    )
    picture: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
        default="https://www.gravatar.com/avatar/?d=identicon",
    )
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    scopes: Mapped[list[AclPrivilege]] = mapped_column(
        Scopes,
        nullable=False,
        default=[RoleUser],
    )

    # relationships
    clients: Mapped[list["Client"]] = relationship(
        "Client", secondary="user_client", back_populates="users", lazy="selectin"
    )
    notes: Mapped[list["Note"]] = relationship(
        "Note", back_populates="user", lazy="selectin"
    )
    ipaddresses: Mapped[list["Ipaddress"]] = relationship(
        "Ipaddress", secondary="user_ipaddress", back_populates="users"
    )
    file_assets: Mapped[list["FileAsset"]] = relationship(
        "FileAsset",
        back_populates="user",
    )

    # properties as methods
    def privileges(self) -> list[AclPrivilege]:
        """
        Returns a list of user privileges to access permission restricted
        resources via ACL.
        """
        principals: list[AclPrivilege]
        principals = [AclPrivilege(f"user:{self.id}")]
        principals.extend([AclPrivilege(sco) for sco in self.scopes])
        return principals

    # ACL
    def __acl__(
        self,
    ) -> list[Tuple[AclAction, AclPrivilege, AclPermission]]:  # pragma: no cover
        return [
            # list
            (AclAction.allow, RoleAdmin, AccessList),
            (AclAction.allow, RoleManager, AccessList),
            # create
            (AclAction.allow, RoleAdmin, AccessCreate),
            # read
            (AclAction.allow, RoleAdmin, AccessRead),
            (AclAction.allow, RoleManager, AccessRead),
            (AclAction.allow, AclPrivilege(f"user:{self.id}"), AccessReadSelf),
            # update
            (AclAction.allow, RoleAdmin, AccessUpdate),
            (AclAction.allow, RoleManager, AccessUpdate),
            (AclAction.allow, AclPrivilege(f"user:{self.id}"), AccessUpdateSelf),
            # delete
            (AclAction.allow, RoleAdmin, AccessDelete),
            (AclAction.allow, RoleUser, AccessDeleteSelf),
        ]

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = "User(%s, Act[%s] Val[%s] Sup[%s] Sco[%d])" % (
            self.username,
            self.is_active,
            self.is_verified,
            self.is_superuser,
            len(self.scopes),
        )
        return repr_str
