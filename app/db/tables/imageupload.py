from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import Mapped, backref, relationship

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .geocoord import GeoCoord  # noqa: F401


class ImageUpload(TableBase):
    __tablename__: str = "imageupload"
    file_name: Mapped[str] = Column(String(120), nullable=False, default="default.jpg")
    file_path: Mapped[str] = Column(String(255), nullable=False, default="uploads/tmp")
    title: Mapped[str] = Column(String(255), nullable=True)
    caption: Mapped[str] = Column(String(255), nullable=True)
    is_geotagged: Mapped[bool] = Column(Boolean(), nullable=True, default=False)

    # relationships
    user_id: Mapped[UUID] = Column(GUID, ForeignKey("user.id"), nullable=True)
    geocoord_id: Mapped[UUID] = Column(GUID, ForeignKey("geocoord.id"), nullable=True)
    geotag: Mapped[Optional[List["GeoCoord"]]] = relationship(
        "GeoCoord", backref=backref("imageupload", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"ImageUpload({self.title}: \
            created {self.created_on}, updated {self.updated_on})"
        return repr_str
