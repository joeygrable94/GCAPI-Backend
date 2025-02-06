from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import JSON, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import JSONType, UUIDType

from app.db.base_class import Base
from app.db.constants import (
    DB_STR_DESC_MAXLEN_INPUT,
    DB_STR_TINYTEXT_MAXLEN_INPUT,
    DB_STR_URLPATH_MAXLEN_INPUT,
)
from app.services.permission import (
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
from app.utilities.uuids import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    from app.entities.organization.model import Organization


class OrganizationStyleguide(Base):
    __tablename__: str = "organization_styleguide"
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
    description: Mapped[str] = mapped_column(
        String(length=DB_STR_DESC_MAXLEN_INPUT), nullable=True
    )
    styleguide: Mapped[JSON | None] = mapped_column(
        JSONType(),
        nullable=True,
        default=None,
    )
    url: Mapped[str | None] = mapped_column(
        String(length=DB_STR_URLPATH_MAXLEN_INPUT),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=True,
    )

    # relationships
    organization_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("organization.id"), nullable=False
    )
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="styleguides"
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

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"OrganizationStyleguide({self.title})"
        return repr_str
