from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Tuple

from pydantic import UUID4
from sqlalchemy import JSON, Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.security.permissions import (
    AclAction,
    AclPermission,
    AclScope,
    Authenticated,
    RoleAdmin,
    RoleUser,
)
from app.core.security.permissions.core import RoleManager
from app.core.utilities.uuids import get_random_username  # type: ignore
from app.core.utilities.uuids import get_uuid
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
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
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    scopes: Mapped[List[AclScope]] = mapped_column(
        JSON,
        nullable=False,
        default=[RoleUser],
    )

    # relationships
    clients: Mapped[List["Client"]] = relationship(
        "Client", secondary="user_client", back_populates="users", lazy="noload"
    )
    notes: Mapped[List["Note"]] = relationship(backref=backref("user", lazy="noload"))

    # privileges to access permission restricted resources via ACL
    def privileges(self) -> List[AclScope]:
        principals: List[AclScope]
        principals = [AclScope(f"user:{self.id}")]
        principals.extend([AclScope(sco) for sco in self.scopes])
        return principals

    # ACL
    def __acl__(self) -> List[Tuple[AclAction, AclScope, AclPermission]]:
        return [
            # create
            (AclAction.allow, RoleAdmin, AclPermission.create),
            # read
            (AclAction.allow, Authenticated, AclPermission.read),
            # update
            (AclAction.allow, RoleAdmin, AclPermission.update),
            # update
            (AclAction.allow, AclScope(f"user:{self.id}"), AclPermission.update),
            # delete
            (AclAction.allow, RoleAdmin, AclPermission.delete),
            # read_relations
            (AclAction.allow, RoleAdmin, AclPermission.read_relations),
            (AclAction.allow, RoleManager, AclPermission.read_relations),
            (
                AclAction.allow,
                AclScope(f"user:{self.id}"),
                AclPermission.read_relations,
            ),
        ]

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"User({self.username})"
        return repr_str
