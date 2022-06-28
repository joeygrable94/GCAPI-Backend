from typing import TYPE_CHECKING, Any

from sqlalchemy import CHAR, Boolean, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .client import Client  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class WebsiteMap(TableBase):
    __tablename__: str = "website_map"
    title: Column[str] = Column(String(255), nullable=False, default="unnamed")
    file_name: Column[str] = Column(String(120), nullable=False, default="sample.xml")
    file_path: Column[str] = Column(String(255), nullable=False, default="uploads/tmp")
    is_processed: Column[bool] = Column(Boolean(), nullable=False, default=False)

    # relationships
    website_id: Column[str] = Column(CHAR(36), ForeignKey("website.id"), nullable=False)
    pages: Any = relationship(
        "WebsitePage", backref=backref("website_map", lazy="noload")
    )

    def __repr__(self) -> str:
        repr_str: str = (
            f"WebsiteMap({self.title}, Site[{self.website_id}], File[{self.filename}])"
        )
        return repr_str
