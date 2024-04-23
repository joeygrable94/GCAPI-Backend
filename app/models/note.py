from typing import TYPE_CHECKING, Any, List, Tuple

from pydantic import UUID4
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp  # type: ignore
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import (  # type: ignore  # noqa: E501
    AesEngine,
    StringEncryptedType,
)

from app.core.config import settings
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
from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import (
    DB_STR_32BIT_MAXLEN_STORED,
    DB_STR_DESC_MAXLEN_STORED,
    DB_STR_TINYTEXT_MAXLEN_STORED,
)

if TYPE_CHECKING:  # pragma: no cover
    from .client_report import ClientReport  # noqa: F401
    from .user import User  # noqa: F401


class Note(Base, Timestamp):
    __tablename__: str = "note"
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
    title: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_DESC_MAXLEN_STORED,
        ),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        StringEncryptedType(
            Boolean,
            settings.api.encryption_key,
            AesEngine,
            "zeroes",
            length=DB_STR_32BIT_MAXLEN_STORED,
        ),
        nullable=False,
        default=True,
    )

    # relationships
    user_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("user.id"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="notes")
    client_reports: Mapped[List["ClientReport"]] = relationship(
        "ClientReport", secondary="client_report_note", back_populates="notes"
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
            (AclAction.allow, RoleUser, AccessReadSelf),
            # update
            (AclAction.allow, RoleAdmin, AccessUpdate),
            (AclAction.allow, RoleManager, AccessUpdate),
            (AclAction.allow, RoleUser, AccessUpdateSelf),
            # delete
            (AclAction.allow, RoleAdmin, AccessDelete),
            (AclAction.allow, RoleManager, AccessDelete),
            (AclAction.allow, RoleUser, AccessDeleteSelf),
        ]

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Item({self.title} by {self.user_id})"
        return repr_str
