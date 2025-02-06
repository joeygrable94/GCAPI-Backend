from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType

from app.db.base_class import Base
from app.utilities.uuids import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    pass


class OrganizationPlatform(Base):
    __tablename__: str = "organization_platform"
    __table_args__: dict = {"mysql_engine": "InnoDB"}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        primary_key=True,
        nullable=False,
        default=get_uuid,
    )
    organization_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("organization.id"),
        nullable=False,
    )
    platform_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("platform.id"),
        nullable=False,
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"OrganizationPlatform({self.id}, [C({self.organization_id}), P({self.platform_id})])"
        return repr_str
