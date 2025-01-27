from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp, UUIDType

from app.core.security.permissions import (
    AccessCreate,
    AccessDelete,
    AccessList,
    AccessRead,
    AccessUpdate,
    AclAction,
    AclPermission,
    AclPrivilege,
    RoleUser,
)
from app.core.utilities import get_uuid
from app.db.base_class import Base
from app.db.custom_types import LongText

if TYPE_CHECKING:  # pragma: no cover
    from .website import Website  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsiteKeywordCorpus(Base, Timestamp):
    __tablename__: str = "website_keywordcorpus"
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
    corpus: Mapped[str] = mapped_column(LongText, nullable=False, default="")
    rawtext: Mapped[str] = mapped_column(LongText, nullable=False, default="")

    # relationships
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("website.id"),
        nullable=False,
    )
    website: Mapped["Website"] = relationship("Website", back_populates="keywordcorpus")
    page_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website_page.id"), nullable=False
    )
    page: Mapped["WebsitePage"] = relationship(
        "WebsitePage", back_populates="keywordcorpus"
    )

    # ACL
    def __acl__(
        self,
    ) -> list[tuple[AclAction, AclPrivilege, AclPermission]]:  # pragma: no cover
        return [
            # list
            (AclAction.allow, RoleUser, AccessList),
            # create
            (AclAction.allow, RoleUser, AccessCreate),
            # read
            (AclAction.allow, RoleUser, AccessRead),
            # update
            (AclAction.allow, RoleUser, AccessUpdate),
            # delete
            (AclAction.allow, RoleUser, AccessDelete),
        ]

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"KeywordCorpus({self.id}, Site[{self.website_id}], Pg[{self.page_id}])"
        )
        return repr_str
