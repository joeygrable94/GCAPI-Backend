from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.tables.base import TableBase
from app.db.types import GUID

if TYPE_CHECKING:  # pragma: no cover
    from .geocoord import GeoCoord  # noqa: F401
    from .user import User  # noqa: F401


class IpAddress(TableBase):
    __tablename__: str = "ipaddress"
    address: Column[str] = Column(
        String(64), unique=True, nullable=False, default="::1"
    )
    is_blocked: Column[bool] = Column(Boolean, nullable=False, default=False)
    isp: Column[Optional[str]] = Column(String(255), nullable=True)
    location: Column[Optional[str]] = Column(String(500), nullable=True)

    # relationships
    geocoord_id: Column[Optional[UUID]] = Column(
        GUID, ForeignKey("geocoord.id"), nullable=True
    )
    users: Column[Optional[List["User"]]] = relationship(  # type: ignore
        "User", secondary="user_ipaddress", back_populates="ip_addresses"
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"IpAddress({self.address})"
        return repr_str
