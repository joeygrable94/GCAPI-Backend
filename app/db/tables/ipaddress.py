"""

Stack Overflow on IP Address Representation:
- https://stackoverflow.com/questions/166132/maximum-length-of-the-textual-representation-of-an-ipv6-address#:~:text=IPv6%20addresses%20are%20normally%20written,So%20that's%2039%20characters%20max.

"""
from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey, String

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .geocoord import GeoCoord  # noqa: F401


class IpAddress(TableBase):
    __tablename__ = "ipaddress"
    address = Column(String(64), unique=True, nullable=False, default="::1")
    isp = Column(String(255), nullable=True)
    location = Column(String(500), nullable=True)

    # relationships
    geocoord_id = Column(CHAR(36), ForeignKey("geocoord.id"), nullable=True)

    def __repr__(self):
        repr_str = f"IpAddress({self.address})"
        return repr_str
