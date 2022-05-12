from typing import TYPE_CHECKING

from sqlalchemy import Column, String

from app.core.models.table_model import TableBase

if TYPE_CHECKING:
    pass


class GeoCoord(TableBase):
    __tablename__           = 'geo_coord'
    address                 = Column(String(1200), nullable=False, default='135-145, South Olive Street, Orange, Orange County, California, 92866, United States')
    latitude                = Column(String(24), nullable=False, default='33.78701447619846')
    longitude               = Column(String(24), nullable=False, default='-117.85381761348981')

    def __repr__(self):
        repr_str = f'GeoCoords({self.latitude}, {self.longitude})'
        return repr_str
