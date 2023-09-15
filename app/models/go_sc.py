from datetime import datetime
from typing import TYPE_CHECKING, Any, List

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .go_sc_country import GoogleSearchConsoleCountry  # noqa: F401
    from .go_sc_device import GoogleSearchConsoleDevice  # noqa: F401
    from .go_sc_page import GoogleSearchConsolePage  # noqa: F401
    from .go_sc_query import GoogleSearchConsoleQuery  # noqa: F401
    from .go_sc_searchappearance import (  # noqa: F401
        GoogleSearchConsoleSearchAppearance,
    )
    from .website import Website  # noqa: F401


class GoogleSearchConsoleProperty(Base):
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
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # relationships
    client_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("client.id"), nullable=False
    )
    website_id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False), ForeignKey("website.id"), nullable=False
    )
    gsc_countries: Mapped[List["GoogleSearchConsoleCountry"]] = relationship(
        "GoogleSearchConsoleCountry",
        backref=backref("go_sc", lazy="noload"),
    )
    gsc_devices: Mapped[List["GoogleSearchConsoleDevice"]] = relationship(
        "GoogleSearchConsoleDevice",
        backref=backref("go_sc", lazy="noload"),
    )
    gsc_pages: Mapped[List["GoogleSearchConsolePage"]] = relationship(
        "GoogleSearchConsolePage",
        backref=backref("go_sc", lazy="noload"),
    )
    gsc_queries: Mapped[List["GoogleSearchConsoleQuery"]] = relationship(
        "GoogleSearchConsoleQuery",
        backref=backref("go_sc", lazy="noload"),
    )
    gsc_searchappearances: Mapped[
        List["GoogleSearchConsoleSearchAppearance"]
    ] = relationship(
        "GoogleSearchConsoleSearchAppearance",
        backref=backref("go_sc", lazy="noload"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoogleSearchConsoleProperty({self.title}, \
            Client[{self.client_id}] Website[{self.website_id}])"
        return repr_str
