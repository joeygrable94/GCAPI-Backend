from typing import TYPE_CHECKING, Any, List, Optional
from uuid import UUID

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import Mapped, backref, relationship

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsiteMap(TableBase):
    __tablename__: str = "website_map"
    title: Mapped[str] = Column(String(255), nullable=False, default="unnamed")
    file_name: Mapped[str] = Column(String(120), nullable=False, default="sample.xml")
    file_path: Mapped[str] = Column(String(255), nullable=False, default="uploads/tmp")
    is_processed: Mapped[bool] = Column(Boolean(), nullable=False, default=False)

    # relationships
    website_id: Mapped[UUID] = Column(GUID, ForeignKey("website.id"), nullable=False)
    pages: Mapped[Optional[List[Any]]] = relationship(
        "WebsitePage", backref=backref("website_map", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"WebsiteMap({self.title}, Site[{self.website_id}], File[{self.file_name}])"
        )
        return repr_str
