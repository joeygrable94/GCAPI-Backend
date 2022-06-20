from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Boolean, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    pass


class ImageUpload(TableBase):
    __tablename__ = "imageupload"
    filename = Column(String(120), nullable=False, default="default.jpg")
    filepath = Column(String(255), nullable=False, default="uploads/tmp")
    title = Column(String(255), nullable=True)
    caption = Column(String(255), nullable=True)
    is_geotagged = Column(Boolean(), nullable=True, default=False)

    # relationships
    user_id = Column(CHAR(36), ForeignKey("user.id"), nullable=False)
    geocoord_id = Column(CHAR(36), ForeignKey("geocoord.id"), nullable=True)
    geotag = relationship("GeoCoord", backref=backref("imageupload", lazy="noload"))

    def __repr__(self):
        repr_str = f"ImageUpload({self.title}: created {self.created_on}, updated {self.updated_on})"
        return repr_str
