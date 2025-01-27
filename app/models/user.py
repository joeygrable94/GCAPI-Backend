from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp, UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import (
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
from app.core.utilities import get_random_username, get_uuid
from app.db.base_class import Base
from app.db.constants import (
    DB_STR_32BIT_MAXLEN_STORED,
    DB_STR_SHORTTEXT_MAXLEN_STORED,
    DB_STR_TINYTEXT_MAXLEN_INPUT,
    DB_STR_TINYTEXT_MAXLEN_STORED,
    DB_STR_USER_PICTURE_DEFAULT,
)
from app.db.custom_types import Scopes

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .ipaddress import Ipaddress  # noqa: F401


class User(Base, Timestamp):
    __tablename__: str = "user"
    __table_args__: dict = {"mysql_engine": "InnoDB"}
    __mapper_args__: dict = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid,
    )
    auth_id: Mapped[str] = mapped_column(
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
    email: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_SHORTTEXT_MAXLEN_STORED,
        ),
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        String(length=DB_STR_TINYTEXT_MAXLEN_INPUT),
        index=True,
        unique=True,
        nullable=False,
        default=get_random_username(),
    )
    picture: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_SHORTTEXT_MAXLEN_STORED,
        ),
        nullable=False,
        default=DB_STR_USER_PICTURE_DEFAULT,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=True,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False,
    )
    is_superuser: Mapped[bool] = mapped_column(
        StringEncryptedType(
            Boolean,
            settings.api.encryption_key,
            AesEngine,
            "zeroes",
            length=DB_STR_32BIT_MAXLEN_STORED,
        ),
        nullable=False,
        default=False,
    )
    scopes: Mapped[list[AclPrivilege]] = mapped_column(
        Scopes(),
        nullable=False,
        default=[RoleUser],
    )

    # relationships
    clients: Mapped[list["Client"]] = relationship(
        "Client", secondary="user_client", back_populates="users"
    )
    ipaddresses: Mapped[list["Ipaddress"]] = relationship(
        "Ipaddress", secondary="user_ipaddress", back_populates="users"
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
    ) -> list[tuple[AclAction, AclPrivilege, AclPermission]]:  # pragma: no cover
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
