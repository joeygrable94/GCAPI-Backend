from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .geocoord import Geocoord  # noqa: F401
    from .user import User  # noqa: F401


class Ipaddress(Base):
    __tablename__: str = "ipaddress"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.current_timestamp(),
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
    address: Mapped[str] = mapped_column(
        String(40), nullable=False, unique=True, primary_key=True, default="::1"
    )
    isp: Mapped[str] = mapped_column(
        String(255), nullable=True, index=True, default="unknown"
    )
    location: Mapped[str] = mapped_column(
        String(255), nullable=True, index=True, default="unknown"
    )

    # relationships
    geocoord_id: Mapped[Optional[UUID4]] = mapped_column(
        UUIDType(binary=False), ForeignKey("geocoord.id"), nullable=True
    )
    geotag: Mapped[Optional["Geocoord"]] = relationship(
        "Geocoord", back_populates="ipaddresses"
    )
    users: Mapped[List["User"]] = relationship(
        "User", secondary="user_ipaddress", back_populates="ipaddresses"
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Ipaddress({self.address} by ISP: {self.isp})"
        return repr_str
