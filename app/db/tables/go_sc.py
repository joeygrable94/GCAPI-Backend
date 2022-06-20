from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:
    from go_sc_country import GoogleSearchConsoleCountry  # noqa: F401
    from go_sc_device import GoogleSearchConsoleDevice  # noqa: F401
    from go_sc_page import GoogleSearchConsolePage  # noqa: F401
    from go_sc_query import GoogleSearchConsoleQuery  # noqa: F401
    from go_sc_searchappearance import \
        GoogleSearchConsoleSearchAppearance  # noqa: F401

    from .client import Client  # noqa: F401
    from .website import Website  # noqa: F401


class GoogleSearchConsoleProperty(TableBase):
    __tablename__ = "go_sc"
    title = Column(String(255), nullable=False)

    # relationships
    client_id = Column(CHAR(36), ForeignKey("client.id"), nullable=False)
    website_id = Column(CHAR(36), ForeignKey("website.id"), nullable=False)
    gsc_countries = relationship(
        "GoogleSearchConsoleCountry",
        backref=backref("go_sc", lazy="noload"),
    )
    gsc_devices = relationship(
        "GoogleSearchConsoleDevice",
        backref=backref("go_sc", lazy="noload"),
    )
    gsc_pages = relationship(
        "GoogleSearchConsolePage",
        backref=backref("go_sc", lazy="noload"),
    )
    gsc_queries = relationship(
        "GoogleSearchConsoleQuery",
        backref=backref("go_sc", lazy="noload"),
    )
    gsc_searchappearances = relationship(
        "GoogleSearchConsoleSearchAppearance",
        backref=backref("go_sc", lazy="noload"),
    )

    def __repr__(self) -> str:
        repr_str = f"GoogleSearchConsoleProperty({self.title}, Client[{self.client_id}] Website[{self.website_id}])"
        return repr_str
