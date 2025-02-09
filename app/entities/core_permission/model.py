from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import JSONType, UUIDType

from app.db.base_class import Base
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.services.permission import (
    AccessCreate,
    AccessDelete,
    AccessList,
    AccessRead,
    AccessUpdate,
    AclAction,
    AclPermission,
    AclPrivilege,
    RoleAdmin,
    RoleUser,
)
from app.utilities.uuids import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    pass


class Permission(Base):
    __tablename__: str = "permission"
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
    spec: Mapped[JSON] = mapped_column(
        JSONType(),
        nullable=False,
    )

    def __acl__(
        self,
    ) -> list[tuple[AclAction, AclPrivilege, AclPermission]]:  # pragma: no cover
        return [
            # list
            (AclAction.allow, RoleAdmin, AccessList),
            (AclAction.allow, RoleUser, AccessList),
            # create
            (AclAction.allow, RoleAdmin, AccessCreate),
            # read
            (AclAction.allow, RoleAdmin, AccessRead),
            (AclAction.allow, RoleUser, AccessRead),
            # update
            (AclAction.allow, RoleAdmin, AccessUpdate),
            # delete
            (AclAction.allow, RoleAdmin, AccessDelete),
        ]

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Permission({self.title})"
        return repr_str
