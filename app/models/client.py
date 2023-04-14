from datetime import datetime
from typing import TYPE_CHECKING, Any, List

from pydantic import UUID4
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from app.core.utilities.uuids import get_uuid  # type: ignore
from app.db.base_class import Base

if TYPE_CHECKING:  # pragma: no cover
    from .client_website import ClientWebsite  # noqa: F401
    from .go_a4 import GoogleAnalytics4Property  # noqa: F401
    from .go_cloud import GoogleCloudProperty  # noqa: F401
    from .go_ua import GoogleUniversalAnalyticsProperty  # noqa: F401
    from .sharpspring import SharpSpring  # noqa: F401
    from .website import Website  # noqa: F401


class Client(Base):
    __tablename__: str = "client"
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
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
    title: Mapped[str] = mapped_column(String(96), nullable=False)
    content: Mapped[str] = mapped_column(String(255), nullable=True)

    # relationships
    websites: Mapped[List["Website"]] = relationship(
        "Website", secondary="client_website", back_populates="clients"
    )
    gcloud_accounts: Mapped[List["GoogleCloudProperty"]] = relationship(
        "GoogleCloudProperty", backref=backref("client", lazy="noload")
    )
    ga4_accounts: Mapped[List["GoogleAnalytics4Property"]] = relationship(
        "GoogleAnalytics4Property", backref=backref("client", lazy="noload")
    )
    gua_accounts: Mapped[List["GoogleUniversalAnalyticsProperty"]] = relationship(
        "GoogleUniversalAnalyticsProperty", backref=backref("client", lazy="noload")
    )
    sharpspring_accounts: Mapped[List["SharpSpring"]] = relationship(
        "SharpSpring", backref=backref("client", lazy="noload")
    )

    def __repr__(self) -> str:  # pragma: no cover
        repr_str: str = f"Client({self.title}, since {self.created_on})"
        return repr_str
