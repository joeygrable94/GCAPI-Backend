from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import backref, relationship

from app.db.tables.base import TableBase

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .client_website import ClientWebsite  # noqa: F401
    from .website_map import WebsiteMap  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class Website(TableBase):
    __tablename__: str = "website"
    domain: Column = Column(String(255), nullable=False)
    is_secure: Column = Column(Boolean(), nullable=False, default=False)

    # relationships
    clients: Any = relationship(
        "Client", secondary="client_website", back_populates="websites"
    )
    sitemaps: Any = relationship(
        "WebsiteMap", backref=backref("website", lazy="noload")
    )
    pages: Any = relationship("WebsitePage", backref=backref("website", lazy="noload"))

    def get_link(self) -> str:  # pragma: no cover
        return f"https://{self.domain}" if self.is_secure else f"http://{self.domain}"

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Website({self.id}, URL[{self.domain}])"
        return repr_str
