from typing import TYPE_CHECKING, Any, List

from pydantic import UUID4
from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp  # type: ignore
from sqlalchemy_utils import UUIDType

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import DB_FLOAT_MAXLEN_STORED, DB_STR_TINYTEXT_MAXLEN_STORED

if TYPE_CHECKING:  # pragma: no cover
    from .file_asset import FileAsset  # noqa: F401
    from .gcft_snap import GcftSnap  # noqa: F401
    from .ipaddress import Ipaddress  # noqa: F401


class Geocoord(Base, Timestamp):
    __tablename__: str = "geocoord"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        unique=True,
        nullable=False,
        default=get_uuid(),
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
    file_assets: Mapped[List["FileAsset"]] = relationship(
        "FileAsset",
        back_populates="geotag",
    )
    gcft_snaps: Mapped[List["GcftSnap"]] = relationship(
        "GcftSnap", back_populates="geotag"
    )
    ipaddresses: Mapped[List["Ipaddress"]] = relationship(
        "Ipaddress", back_populates="geotag"
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Geocoords({self.latitude}, {self.longitude})"
        return repr_str
