from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType

from app.db.base_class import Base
from app.utilities.uuids import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    pass


class WebsiteGoAnalytics4Property(Base):
    __tablename__: str = "website_go_a4"
    __table_args__: dict = {"mysql_engine": "InnoDB"}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        primary_key=True,
        nullable=False,
        default=get_uuid,
    )
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("website.id"),
        nullable=False,
    )
    go_a4_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("go_a4.id"),
        nullable=False,
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"WebsiteGoAnalytics4Property({self.id}, [W({self.website_id}), GA4({self.go_a4_id})])"
        return repr_str
