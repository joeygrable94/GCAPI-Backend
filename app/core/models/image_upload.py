from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.models.table_model import TableBase

if TYPE_CHECKING:
    from .user import User
    from .geo_coord import GeoCoord


class ImageUpload(TableBase):
    __tablename__           = 'image_upload'
    filename                = Column(String(120), nullable=False, default='default.jpg')
    filepath                = Column(String(255), nullable=False, default='uploads/tmp')
    title                   = Column(String(255), nullable=True)
    caption                 = Column(String(255), nullable=True)
    # uploaded by
    user_id                 = Column(CHAR(36), ForeignKey('user.id'), nullable=False)
    # geotag metadata
    is_geotagged            = Column(Boolean(), nullable=True, default=False)
    geo_coord_id            = Column(CHAR(36), ForeignKey('geo_coord.id'), nullable=True)
    geo_data                = relationship('GeoCoord')

    def __repr__(self):
        repr_str = f'ImageUpload({self.filename}: created {self.created_on}, updated {self.updated_on})'
        return repr_str

