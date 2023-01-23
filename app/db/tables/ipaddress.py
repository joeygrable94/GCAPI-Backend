from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .geocoord import GeoCoord  # noqa: F401


class IpAddress(TableBase):
    __tablename__: str = "ipaddress"
    address: Mapped[str] = Column(
        String(64), unique=True, nullable=False, default="::1"
    )
    isp: Mapped[str] = Column(String(255), nullable=True)
    location: Mapped[str] = Column(String(500), nullable=True)

    # relationships
    geocoord_id: Mapped[UUID] = Column(GUID, ForeignKey("geocoord.id"), nullable=True)

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"IpAddress({self.address})"
        return repr_str
