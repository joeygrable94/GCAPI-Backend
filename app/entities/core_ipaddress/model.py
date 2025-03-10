from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import IPAddressType, UUIDType

from app.db.base_class import Base
from app.db.constants import (
    DB_STR_16BIT_MAXLEN_INPUT,
    DB_STR_32BIT_MAXLEN_INPUT,
    DB_STR_64BIT_MAXLEN_INPUT,
    DB_STR_TINYTEXT_MAXLEN_INPUT,
    DB_STR_URLPATH_MAXLEN_INPUT,
)
from app.utilities.uuids import get_uuid

if TYPE_CHECKING:  # pragma: no cover
    from app.entities.core_audit_log.model import AuditLog
    from app.entities.core_geocoord.model import Geocoord
    from app.entities.core_user.model import User


class Ipaddress(Base):
    __tablename__: str = "ipaddress"
    __table_args__: dict = {"mysql_engine": "InnoDB"}
    __mapper_args__: dict = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        primary_key=True,
        nullable=False,
        default=get_uuid,
    )
    address: Mapped[str] = mapped_column(
        IPAddressType(),
        index=True,
        unique=True,
        nullable=False,
        default="127.0.0.1",
    )
    hostname: Mapped[str] = mapped_column(
        String(length=DB_STR_TINYTEXT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    is_anycast: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=True,
        default=None,
    )
    city: Mapped[str] = mapped_column(
        String(length=DB_STR_TINYTEXT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    region: Mapped[str] = mapped_column(
        String(length=DB_STR_TINYTEXT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    country: Mapped[str] = mapped_column(
        String(length=DB_STR_16BIT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    loc: Mapped[str] = mapped_column(
        String(length=DB_STR_32BIT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    org: Mapped[str] = mapped_column(
        String(length=DB_STR_TINYTEXT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    postal: Mapped[str] = mapped_column(
        String(length=DB_STR_16BIT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    timezone: Mapped[str] = mapped_column(
        String(length=DB_STR_64BIT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    country_name: Mapped[str] = mapped_column(
        String(length=DB_STR_TINYTEXT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    is_eu: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=True,
        default=None,
    )
    country_flag_url: Mapped[str] = mapped_column(
        String(length=DB_STR_URLPATH_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    country_flag_unicode: Mapped[str] = mapped_column(
        String(length=DB_STR_URLPATH_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    country_currency_code: Mapped[str] = mapped_column(
        String(length=DB_STR_16BIT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    continent_code: Mapped[str] = mapped_column(
        String(length=DB_STR_16BIT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    continent_name: Mapped[str] = mapped_column(
        String(length=DB_STR_16BIT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    latitude: Mapped[str] = mapped_column(
        String(length=DB_STR_16BIT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )
    longitude: Mapped[str] = mapped_column(
        String(length=DB_STR_16BIT_MAXLEN_INPUT),
        nullable=True,
        default=None,
    )

    # relationships
    geocoords: Mapped[list["Geocoord"]] = relationship(
        "Geocoord",
        secondary="ipaddress_geocoord",
        back_populates="ipaddresses",
    )
    users: Mapped[list["User"]] = relationship(
        "User", secondary="user_ipaddress", back_populates="ipaddresses"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog", back_populates="ipaddress"
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Ipaddress({self.address} by ISP: {self.hostname})"
        return repr_str
