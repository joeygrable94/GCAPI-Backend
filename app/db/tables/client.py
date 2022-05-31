from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Text

from app.db.tables.base import TableBase

# from sqlalchemy.orm import backref, relationship


if TYPE_CHECKING:
    # from .service import Service  # noqa: F401
    # from .web_site import WebSite  # noqa: F401
    pass


class Client(TableBase):
    __tablename__ = "client"
    title = Column(String(96), nullable=False)
    content = Column(Text, nullable=True)
    # web_sites = relationship(
    #     'WebSite',
    #     backref=backref('client', lazy=True)
    # )
    # services = relationship(
    #     'Service',
    #     secondary='client_service',
    #     backref=backref('client', lazy=True)
    # )
    # dmarc_reports = relationship(
    #     'DmarcReport',
    #     backref=backref('client', lazy=True),
    #     cascade='save-update'
    # )

    def __repr__(self) -> str:
        repr_str = f"Client({self.title}, since {self.created_on})"
        return repr_str
