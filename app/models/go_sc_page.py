from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Tuple

from pydantic import UUID4
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
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
from app.db.constants import DB_FLOAT_MAXLEN_STORED, DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.custom_types import LongText

if TYPE_CHECKING:  # pragma: no cover
    from .go_sc import GoSearchConsoleProperty  # noqa: F401


class GoSearchConsolePage(Base, Timestamp):
    __tablename__: str = "go_sc_page"
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
        nullable=False,
    )
    keys: Mapped[str] = mapped_column(LongText, nullable=False, default="")
    clicks: Mapped[int] = mapped_column(Integer, nullable=False)
    impressions: Mapped[int] = mapped_column(Integer, nullable=False)
    ctr: Mapped[float] = mapped_column(Float(DB_FLOAT_MAXLEN_STORED), nullable=False)
    position: Mapped[float] = mapped_column(
        Float(DB_FLOAT_MAXLEN_STORED), nullable=False
    )
    date_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    date_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # relationships
    gsc_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("go_sc.id"), nullable=False
    )
    gsc_account: Mapped["GoSearchConsoleProperty"] = relationship(
        "GoSearchConsoleProperty", back_populates="gsc_pages"
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

    # represenation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"GoSearchConsolePage(GSCID[{self.gsc_id}], \
            C={self.clicks} I={self.impressions} CTR={self.ctr} Pos={self.position})"
        )
        return repr_str
