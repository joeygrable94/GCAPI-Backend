from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import Timestamp, UUIDType

from app.db.base_class import Base
from app.utilities import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    pass


class WebsiteGoAdsProperty(Base, Timestamp):
    __tablename__: str = "website_go_ads"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid,
    )
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("website.id"),
        primary_key=True,
        nullable=False,
    )
    go_ads_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("go_ads.id"),
        primary_key=True,
        nullable=False,
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"WebsiteGoAdsProperty({self.id}, [W({self.website_id}), GAds({self.go_ads_id})])"
        return repr_str
