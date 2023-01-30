from decimal import Decimal
from typing import TYPE_CHECKING, Union

from sqlalchemy import Column, Float, String

from app.db.tables.base import TableBase

if TYPE_CHECKING:  # pragma: no cover
    pass


class GeoCoord(TableBase):
    __tablename__: str = "geocoord"
    address: Column[str] = Column(
        String(500),
        nullable=False,
        default="135-145, South Olive Street, Orange, \
            Orange County, California, 92866, United States",
    )
    latitude: Column[Union[float, Decimal]] = Column(
        Float(20), nullable=False, default=33.7870144761984600
    )
    longitude: Column[Union[float, Decimal]] = Column(
        Float(20), nullable=False, default=-117.853817613489810
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GeoCoords({self.latitude}, {self.longitude})"
        return repr_str
