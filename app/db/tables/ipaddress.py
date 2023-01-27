from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .geocoord import GeoCoord  # noqa: F401


class IpAddress(TableBase):
    __tablename__: str = "ipaddress"
    address: Column[str] = Column(
        String(64), unique=True, nullable=False, default="::1"
    )
    isp: Column[Optional[str]] = Column(String(255), nullable=True)
    location: Column[Optional[str]] = Column(String(500), nullable=True)

    # relationships
    geocoord_id: Column[Optional[UUID]] = Column(
        GUID, ForeignKey("geocoord.id"), nullable=True
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"IpAddress({self.address})"
        return repr_str
