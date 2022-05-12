from typing import TYPE_CHECKING

from sqlalchemy import Column, String

from app.core.models.table_model import TableBase

if TYPE_CHECKING:
    pass


class IpAddress(TableBase):
    __tablename__           = 'ip_address'
    address                 = Column(String(64), unique=True, nullable=False)
    isp                     = Column(String(255), nullable=True)
    location                = Column(String(255), nullable=True)
    geocoord                = Column(String(255), nullable=True)

    def __repr__(self):
        repr_str = f'IpAddress({self.address})'
        return repr_str
