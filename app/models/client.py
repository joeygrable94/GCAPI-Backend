from typing import TYPE_CHECKING, Any, List, Tuple

from pydantic import UUID4
from sqlalchemy import JSON, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp  # type: ignore
from sqlalchemy_utils import JSONType, UUIDType
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
from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import (
    DB_STR_64BIT_MAXLEN_INPUT,
    DB_STR_DESC_MAXLEN_STORED,
    DB_STR_TINYTEXT_MAXLEN_INPUT,
)

if TYPE_CHECKING:  # pragma: no cover
    from .bdx_feed import BdxFeed  # noqa: F401
    from .client_report import ClientReport  # noqa: F401
    from .data_bucket import DataBucket  # noqa: F401
    from .file_asset import FileAsset  # noqa: F401
    from .gcft import Gcft  # noqa: F401
    from .go_a4 import GoAnalytics4Property  # noqa: F401
    from .go_cloud import GoCloudProperty  # noqa: F401
    from .go_sc import GoSearchConsoleProperty  # noqa: F401
    from .sharpspring import Sharpspring  # noqa: F401
    from .tracking_link import TrackingLink  # noqa: F401
    from .user import User  # noqa: F401
    from .website import Website  # noqa: F401


class Client(Base, Timestamp):
    __tablename__: str = "client"
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
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_DESC_MAXLEN_STORED,
        ),
        nullable=True,
    )
    style_guide: Mapped[JSON] = mapped_column(
        JSONType,
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=True,
    )

    # relationships
    users: Mapped[List["User"]] = relationship(
        "User", secondary="user_client", back_populates="clients"
    )
    data_bucket: Mapped["DataBucket"] = relationship(
        "DataBucket", back_populates="client", lazy="joined"
    )
    file_assets: Mapped[List["FileAsset"]] = relationship(
        "FileAsset",
        back_populates="client",
    )
    websites: Mapped[List["Website"]] = relationship(
        secondary="client_website", back_populates="clients", cascade="all, delete"
    )
    client_reports: Mapped[List["ClientReport"]] = relationship(
        "ClientReport", back_populates="client"
    )
    tracking_links: Mapped[List["TrackingLink"]] = relationship(
        "TrackingLink", back_populates="client"
    )
    gcloud_accounts: Mapped[List["GoCloudProperty"]] = relationship(
        "GoCloudProperty", back_populates="client", cascade="all, delete-orphan"
    )
    gsc_accounts: Mapped[List["GoSearchConsoleProperty"]] = relationship(
        "GoSearchConsoleProperty", back_populates="client", cascade="all, delete-orphan"
    )
    ga4_accounts: Mapped[List["GoAnalytics4Property"]] = relationship(
        "GoAnalytics4Property", back_populates="client", cascade="all, delete-orphan"
    )
    sharpspring_accounts: Mapped[List["Sharpspring"]] = relationship(
        "Sharpspring", back_populates="client", cascade="all, delete-orphan"
    )
    bdx_feeds: Mapped[List["BdxFeed"]] = relationship(
        "BdxFeed", back_populates="client", cascade="all, delete-orphan"
    )
    gcflytours: Mapped[List["Gcft"]] = relationship(
        "Gcft", back_populates="client", cascade="all, delete-orphan"
    )

    # ACL
    def __acl__(
        self,
    ) -> List[Tuple[AclAction, AclPrivilege, AclPermission]]:  # pragma: no cover
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
