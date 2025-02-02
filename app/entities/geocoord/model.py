from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp, UUIDType

from app.db.base_class import Base
from app.db.constants import DB_FLOAT_MAXLEN_STORED, DB_STR_TINYTEXT_MAXLEN_STORED
from app.utilities import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    from app.entities.gcft_snap.model import GcftSnap
    from app.entities.ipaddress.model import Ipaddress


class Geocoord(Base, Timestamp):
    __tablename__: str = "geocoord"
    __table_args__: dict = {"mysql_engine": "InnoDB"}
    __mapper_args__: dict = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        unique=True,
        nullable=False,
        default=get_uuid,
    )
    address: Mapped[str] = mapped_column(
        String(DB_STR_TINYTEXT_MAXLEN_STORED),
        unique=True,
        primary_key=True,
        nullable=False,
        default="135-145, South Olive Street, Orange, \
            Orange County, California, 92866, United States",
    )
    latitude: Mapped[float] = mapped_column(
        Float(DB_FLOAT_MAXLEN_STORED), nullable=False, default=33.78701447619846000
    )
    longitude: Mapped[float] = mapped_column(
        Float(DB_FLOAT_MAXLEN_STORED), nullable=False, default=-117.853817613489810
    )

    # relationships
    gcft_snaps: Mapped[list["GcftSnap"]] = relationship(
        "GcftSnap", back_populates="geotag"
    )
    ipaddresses: Mapped[list["Ipaddress"]] = relationship(
        "Ipaddress", back_populates="geotag"
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Geocoords({self.latitude}, {self.longitude})"
        return repr_str
