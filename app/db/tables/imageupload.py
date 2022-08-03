from typing import TYPE_CHECKING, Any, Optional

from fastapi_utils.guid_type import GUID
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:
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
    user_id: Column[str] = Column(GUID, ForeignKey("user.id"), nullable=False)
    geocoord_id: Column[Optional[str]] = Column(
        GUID, ForeignKey("geocoord.id"), nullable=True
    )
    geotag: Any = relationship(
        "GeoCoord", backref=backref("imageupload", lazy="noload")
    )

    def __repr__(self) -> str:
        repr_str: str = f"ImageUpload({self.title}: \
            created {self.created_on}, updated {self.updated_on})"
        return repr_str
