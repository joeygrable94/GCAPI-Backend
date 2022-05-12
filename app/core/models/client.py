from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship, backref

from app.core.models.table_model import TableBase

if TYPE_CHECKING:
    # from .service import Service  # noqa: F401
    # from .web_site import WebSite  # noqa: F401
    pass


class Client(TableBase):
    __tablename__           = 'client'
    key_id                  = Column(String(8), unique=True, nullable=False)
    title                   = Column(String(96))
    content                 = Column(Text)
    # web_sites               = relationship('WebSite', backref=backref('client', lazy=True))
    # services                = relationship('Service', secondary='client_service', backref=backref('client', lazy=True))
    # dmarc_reports           = relationship('DmarcReport', backref=backref('client', lazy=True), cascade='save-update')

    def __repr__(self):
        repr_str = f'Client({self.name}, since {self.created_on})'
        return repr_str
