from datetime import datetime
from typing import TYPE_CHECKING, List

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .website_page import WebsitePage  # noqa: F401


class WebsiteMap(Base):
    __tablename__: str = "website_map"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        index=True,
        nullable=False,
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    url: Mapped[str] = mapped_column(Text, nullable=False, default="/sitemap_index.xml")

    # relationships
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website.id"), nullable=False
    )
    pages: Mapped[List["WebsitePage"]] = relationship(
        "WebsitePage", backref=backref("website_map", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"WebsiteMap({self.url}, Site[{self.website_id}])"
        return repr_str
