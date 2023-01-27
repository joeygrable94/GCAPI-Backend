from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase
from app.db.types import GUID

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


class GoogleSearchConsoleProperty(TableBase):
    __tablename__: str = "go_sc"
    title: Column[str] = Column(String(255), nullable=False)

    # relationships
    client_id: Column[UUID] = Column(GUID, ForeignKey("client.id"), nullable=False)
    website_id: Column[UUID] = Column(GUID, ForeignKey("website.id"), nullable=False)
    gsc_countries: Column[
        Optional[List["GoogleSearchConsoleCountry"]]
    ] = relationship(  # type: ignore
        "GoogleSearchConsoleCountry",
        backref=backref("go_sc", lazy="noload"),
    )
    gsc_devices: Column[
        Optional[List["GoogleSearchConsoleDevice"]]
    ] = relationship(  # type: ignore
        "GoogleSearchConsoleDevice",
        backref=backref("go_sc", lazy="noload"),
    )
    gsc_pages: Column[
        Optional[List["GoogleSearchConsolePage"]]
    ] = relationship(  # type: ignore
        "GoogleSearchConsolePage",
        backref=backref("go_sc", lazy="noload"),
    )
    gsc_queries: Column[
        Optional[List["GoogleSearchConsoleQuery"]]
    ] = relationship(  # type: ignore
        "GoogleSearchConsoleQuery",
        backref=backref("go_sc", lazy="noload"),
    )
    gsc_searchappearances: Column[
        Optional[List["GoogleSearchConsoleSearchAppearance"]]
    ] = relationship(  # type: ignore
        "GoogleSearchConsoleSearchAppearance",
        backref=backref("go_sc", lazy="noload"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"GoogleSearchConsoleProperty({self.title}, \
            Client[{self.client_id}] Website[{self.website_id}])"
        return repr_str
