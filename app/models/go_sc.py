from typing import TYPE_CHECKING, Any, List, Tuple

from pydantic import UUID4
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp  # type: ignore
from sqlalchemy_utils import UUIDType

from app.core.security.permissions import (
    AccessCreate,
    AccessCreateRelated,
    AccessDelete,
    AccessDeleteRelated,
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
from app.core.utilities import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .go_sc_country import GoSearchConsoleCountry  # noqa: F401
    from .go_sc_device import GoSearchConsoleDevice  # noqa: F401
    from .go_sc_page import GoSearchConsolePage  # noqa: F401
    from .go_sc_query import GoSearchConsoleQuery  # noqa: F401
    from .go_sc_searchappearance import GoSearchConsoleSearchappearance  # noqa: F401
    from .website import Website  # noqa: F401


class GoSearchConsoleProperty(Base, Timestamp):
    __tablename__: str = "go_sc"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    title: Mapped[str] = mapped_column(
        String(length=DB_STR_TINYTEXT_MAXLEN_INPUT),
        index=True,
        unique=True,
        nullable=False,
    )

    # relationships
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )
    client: Mapped["Client"] = relationship("Client", back_populates="gsc_accounts")
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website.id"), nullable=False
    )
    website: Mapped["Website"] = relationship("Website", back_populates="gsc_accounts")
    gsc_countries: Mapped[List["GoSearchConsoleCountry"]] = relationship(
        "GoSearchConsoleCountry", back_populates="gsc_account"
    )
    gsc_devices: Mapped[List["GoSearchConsoleDevice"]] = relationship(
        "GoSearchConsoleDevice", back_populates="gsc_account"
    )
    gsc_pages: Mapped[List["GoSearchConsolePage"]] = relationship(
        "GoSearchConsolePage", back_populates="gsc_account"
    )
    gsc_queries: Mapped[List["GoSearchConsoleQuery"]] = relationship(
        "GoSearchConsoleQuery", back_populates="gsc_account"
    )
    gsc_searchappearances: Mapped[List["GoSearchConsoleSearchappearance"]] = (
        relationship("GoSearchConsoleSearchappearance", back_populates="gsc_account")
    )

    # ACL
    def __acl__(
        self,
    ) -> List[Tuple[AclAction, AclPrivilege, AclPermission]]:  # pragma: no cover
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
            (AclAction.allow, RoleEmployee, AccessDeleteRelated),
            (AclAction.allow, RoleClient, AccessDeleteRelated),
        ]

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"GoSearchConsoleProperty({self.title}, Client[{self.client_id}] Website[{self.website_id}])"  # noqa: F841, E501
        )
        return repr_str
