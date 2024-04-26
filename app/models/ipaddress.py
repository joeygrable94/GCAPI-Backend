from typing import TYPE_CHECKING, Any, List, Optional

from pydantic import UUID4
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import IPAddressType  # type: ignore
from sqlalchemy_utils import Timestamp, UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import (  # type: ignore  # noqa: E501
    AesEngine,
    StringEncryptedType,
)

from app.core.config import settings
from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import (
    DB_STR_16BIT_MAXLEN_STORED,
    DB_STR_32BIT_MAXLEN_STORED,
    DB_STR_64BIT_MAXLEN_STORED,
    DB_STR_TINYTEXT_MAXLEN_STORED,
    DB_STR_URLPATH_MAXLEN_STORED,
)

if TYPE_CHECKING:  # pragma: no cover
    from .geocoord import Geocoord  # noqa: F401
    from .user import User  # noqa: F401


class Ipaddress(Base, Timestamp):
    __tablename__: str = "ipaddress"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        unique=True,
        primary_key=True,
        nullable=False,
        default=get_uuid(),
    )
    address: Mapped[str] = mapped_column(
        StringEncryptedType(
            IPAddressType,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        unique=True,
        nullable=False,
        default="127.0.0.1",
    )
    hostname: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    is_anycast: Mapped[bool] = mapped_column(
        StringEncryptedType(
            Boolean,
            settings.api.encryption_key,
            AesEngine,
            "zeroes",
            length=DB_STR_32BIT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    city: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    region: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    country: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_16BIT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    loc: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_32BIT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    org: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    postal: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_16BIT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    timezone: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_64BIT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    country_name: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    is_eu: Mapped[bool] = mapped_column(
        StringEncryptedType(
            Boolean,
            settings.api.encryption_key,
            AesEngine,
            "zeroes",
            length=DB_STR_32BIT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    country_flag_url: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_URLPATH_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    country_flag_unicode: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    country_currency_code: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_16BIT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    continent_code: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_16BIT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    continent_name: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_16BIT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    latitude: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_16BIT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
    )
    longitude: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_16BIT_MAXLEN_STORED,
        ),
        nullable=True,
        default=None,
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
        repr_str: str = f"Ipaddress({self.address} by ISP: {self.hostname})"
        return repr_str
