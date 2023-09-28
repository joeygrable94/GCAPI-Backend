from datetime import datetime
from typing import TYPE_CHECKING, Any, List

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
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
    id: Mapped[UUID4] = mapped_column(
        UUIDType(binary=False),
        index=True,
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
    domain: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, primary_key=True
    )
    is_secure: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

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
