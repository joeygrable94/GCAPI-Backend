from datetime import datetime
from typing import TYPE_CHECKING, List

from pydantic import UUID4
from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client  # noqa: F401
    from .website_map import WebsiteMap  # noqa: F401
    from .website_page import WebsitePage  # noqa: F401


class Website(Base):
    __tablename__: str = "website"
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid(),
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        index=True,
        nullable=False,
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    domain: Mapped[str] = mapped_column(String(255), nullable=False)
    is_secure: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # relationships
    clients: Mapped[List["Client"]] = relationship(
        "Client", secondary="client_website", back_populates="websites"
    )
    sitemaps: Mapped[List["WebsiteMap"]] = relationship(
        "WebsiteMap", backref=backref("website", lazy="noload")
    )
    pages: Mapped[List["WebsitePage"]] = relationship(
        "WebsitePage", backref=backref("website", lazy="noload")
    )

    def get_link(self) -> str:  # pragma: no cover
        return f"https://{self.domain}" if self.is_secure else f"http://{self.domain}"

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Website({self.id}, URL[{self.domain}])"
        return repr_str
