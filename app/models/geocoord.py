from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    pass


class GeoCoord(Base):
    __tablename__: str = "geocoord"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        index=True,
        nullable=False,
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    address: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        default="135-145, South Olive Street, Orange, \
            Orange County, California, 92866, United States",
    )
    latitude: Mapped[float] = mapped_column(
        Float(20), nullable=False, default=33.7870144761984600
    )
    longitude: Mapped[float] = mapped_column(
        Float(20), nullable=False, default=-117.853817613489810
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GeoCoords({self.latitude}, {self.longitude})"
        return repr_str
