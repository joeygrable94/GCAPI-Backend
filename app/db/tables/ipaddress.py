from typing import TYPE_CHECKING, Optional

from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, ForeignKey, String

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from .geocoord import GeoCoord  # noqa: F401


class IpAddress(TableBase):
    __tablename__: str = "ipaddress"
    address: Column[str] = Column(
        String(64), unique=True, nullable=False, default="::1"
    )
    isp: Column[Optional[str]] = Column(String(255), nullable=True)
    location: Column[Optional[str]] = Column(String(500), nullable=True)

    # relationships
    geocoord_id: Column[Optional[str]] = Column(
        GUID, ForeignKey("geocoord.id"), nullable=True
    )

    def __repr__(self) -> str:
        repr_str: str = f"IpAddress({self.address})"
        return repr_str
