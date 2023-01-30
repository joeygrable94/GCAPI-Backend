from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .geocoord import GeoCoord  # noqa: F401


class ImageUpload(TableBase):
    __tablename__: str = "imageupload"
    file_name: Column[str] = Column(String(120), nullable=False, default="default.jpg")
    file_path: Column[str] = Column(String(255), nullable=False, default="uploads/tmp")
    title: Column[Optional[str]] = Column(String(255), nullable=True)
    caption: Column[Optional[str]] = Column(String(255), nullable=True)
    is_geotagged: Column[Optional[bool]] = Column(
        Boolean(), nullable=True, default=False
    )

    # relationships
    user_id: Column[Optional[UUID]] = Column(GUID, ForeignKey("user.id"), nullable=True)
    geocoord_id: Column[Optional[UUID]] = Column(
        GUID, ForeignKey("geocoord.id"), nullable=True
    )
    geotag: Column[Optional[List["GeoCoord"]]] = relationship(  # type: ignore
        "GeoCoord", backref=backref("imageupload", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"ImageUpload({self.title}: \
            created {self.created_on}, updated {self.updated_on})"
        return repr_str
