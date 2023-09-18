from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .geocoord import Geocoord  # noqa: F401


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
    ip: Mapped[str] = mapped_column(
        String(40), nullable=False, unique=True, primary_key=True, default="::1"
    )
    isp: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, default="unknown"
    )
    location: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, default="unknown"
    )

    # relationships
    geocoord_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("geocoord.id"), nullable=True
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Ipaddress({self.ip} by ISP: {self.isp})"
        return repr_str
