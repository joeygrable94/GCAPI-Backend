from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType

from app.db.base_class import Base
from app.utilities.uuids import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    pass


class WebsiteGoAdsProperty(Base):
    __tablename__: str = "website_go_ads"
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
    go_ads_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("go_ads.id"),
        nullable=False,
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"WebsiteGoAdsProperty({self.id}, [W({self.website_id}), GAds({self.go_ads_id})])"
        return repr_str
