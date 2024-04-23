from typing import TYPE_CHECKING, Any, List

from pydantic import UUID4
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Timestamp  # type: ignore
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import (  # type: ignore  # noqa: E501
    AesEngine,
    StringEncryptedType,
)

from app.core.config import settings
from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_STORED

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .go_sc_country import GoSearchConsoleCountry  # noqa: F401
    from .go_sc_device import GoSearchConsoleDevice  # noqa: F401
    from .go_sc_page import GoSearchConsolePage  # noqa: F401
    from .go_sc_query import GoSearchConsoleQuery  # noqa: F401
    from .go_sc_searchappearance import GoSearchConsoleSearchappearance  # noqa: F401
    from .website import Website  # noqa: F401


class GoSearchConsoleProperty(Base, Timestamp):
    __tablename__: str = "go_sc"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    title: Mapped[str] = mapped_column(
        StringEncryptedType(
            String,
            settings.api.encryption_key,
            AesEngine,
            "pkcs5",
            length=DB_STR_TINYTEXT_MAXLEN_STORED,
        ),
        unique=True,
        nullable=False,
    )

    # relationships
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )
    client: Mapped["Client"] = relationship("Client", back_populates="gsc_accounts")
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website.id"), nullable=False
    )
    website: Mapped["Website"] = relationship("Website", back_populates="gsc_accounts")
    gsc_countries: Mapped[List["GoSearchConsoleCountry"]] = relationship(
        "GoSearchConsoleCountry", back_populates="gsc_account"
    )
    gsc_devices: Mapped[List["GoSearchConsoleDevice"]] = relationship(
        "GoSearchConsoleDevice", back_populates="gsc_account"
    )
    gsc_pages: Mapped[List["GoSearchConsolePage"]] = relationship(
        "GoSearchConsolePage", back_populates="gsc_account"
    )
    gsc_queries: Mapped[List["GoSearchConsoleQuery"]] = relationship(
        "GoSearchConsoleQuery", back_populates="gsc_account"
    )
    gsc_searchappearances: Mapped[List["GoSearchConsoleSearchappearance"]] = (
        relationship("GoSearchConsoleSearchappearance", back_populates="gsc_account")
    )

    # representation
    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = (
            f"GoSearchConsoleProperty({self.title}, \
            Client[{self.client_id}] Website[{self.website_id}])"
        )
        return repr_str
